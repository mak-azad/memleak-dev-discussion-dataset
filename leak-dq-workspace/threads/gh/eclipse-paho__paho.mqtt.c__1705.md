# Socket descriptor leak in v1.3.16 release

- URL: https://github.com/eclipse-paho/paho.mqtt.c/issues/1705
- Repo: eclipse-paho/paho.mqtt.c (language: C)
- State: open; created 2026-09-23T19:31:22Z; status ok; passes offcwe

## Issue body

reporter (NONE) · bguan-radionix · 2026-09-23T19:31:22Z · https://github.com/eclipse-paho/paho.mqtt.c/issues/1705

**Describe the bug**

In v1.3.16, commit 375e76d8 (PR #1642, issue #1430) added an internal socketpair() used to wake poll()/select() when connect or close happens on another thread.

Socket_outInitialize() creates that pair and stores the descriptors in sockfd[0] (read end, added to the poll/select set) and sockfd[1] (write end, not tracked there). Destroying the last client runs Socket_outTerminate(), which frees the socket-module lists and buffers but does not close those two descriptors. The next MQTTAsync_create() / MQTTClient_create() calls Socket_outInitialize() → Socket_pair() again, which overwrites sockfd[] and leaks two file descriptors per create/destroy cycle.

Long-running processes that recreate the last client (reconnect loops, failed connect then destroy) grow the process fd count by 2 each cycle and can hit EMFILE / “Too many open files”.

**To Reproduce**
Trace is optional (MQTT_C_CLIENT_TRACE=ON, MQTT_C_CLIENT_TRACE_LEVEL=PROTOCOL as in the README). The leak is easier to see from the process fd count than from protocol logs.

Use Paho C v1.3.16 (libpaho-mqtt3a or libpaho-mqtt3c; SSL is not required).
Ensure no broker is required for the leak; a failed connect still triggers library init/terminate if you destroy the last (or only) client.
Loop: create a client, optionally connect (success or failure), then destroy it. Example with the synchronous API:
```
for (int i = 0; i < 20; ++i) {
    MQTTClient client = NULL;
    MQTTClient_create(&client, "tcp://127.0.0.1:1883", "fd-leak-test",
                      MQTTCLIENT_PERSISTENCE_NONE, NULL);
    MQTTClient_connectOptions opts = MQTTClient_connectOptions_initializer;
    opts.connectTimeout = 1;
    MQTTClient_connect(client, &opts);   /* success or failure both leak */
    MQTTClient_disconnect(client, 0);
    MQTTClient_destroy(&client);
    /* count fds, e.g. entries in /proc/self/fd */
}
```
The same pattern applies to MQTTAsync_create / MQTTAsync_destroy when that client is the last one and the library fully terminates.

Watch `/proc/<pid>/fd` or `lsof -p <pid>`. After each cycle the count increases by 2.


**Expected behavior**
After MQTTClient_destroy() / MQTTAsync_destroy() of the last client, Socket_outTerminate() should close both ends of the interrupt pair and forget the descriptors (INVALID_SOCKET). A later create/initialize should not leave the previous pair open. The process fd count should stay stable across create/destroy cycles.

**Screenshots**
Not applicable.

**Log files**

`lsof/ls -l /proc/<pid>/fd` shows leftover socket:[…] entries that persist after destroy and are not replaced by the new pair.

** Environment (please complete the following information):**
 - OS: Embedded Linux

**Additional context**
Add any other context about the problem here.


## Comment 5928447469

other (CONTRIBUTOR) · matthiasklein · 2026-10-01T09:16:57Z · https://github.com/eclipse-paho/paho.mqtt.c/issues/1705#issuecomment-5928447469

We've also encountered this problem in the field, and it causes us to run out of file descriptors over time.

We're using this patch:

```
--- a/src/Socket.c
+++ b/src/Socket.c
@@ -278,7 +278,7 @@
 
 #endif /* _WIN32 */
 
-static SOCKET sockfd[2];
+static SOCKET sockfd[2] = {INVALID_SOCKET, INVALID_SOCKET};
 
 int Socket_pair()
 {
@@ -293,12 +293,44 @@
 
 int Socket_interrupt()
 {
+	int rc;
+
 	FUNC_ENTRY;
-	int rc = send(sockfd[1], "\0", 1, 0);
+	/* the pair is closed by Socket_outTerminate, and Socket_close_only can
+	   still run afterwards, so the write end must be checked here */
+	if (sockfd[1] == INVALID_SOCKET)
+		rc = SOCKET_ERROR;
+	else
+		rc = send(sockfd[1], "\0", 1, 0);
 	FUNC_EXIT_RC(rc);
 	return rc;
 }
 
+
+/**
+ * Close both ends of the interrupt pair created by Socket_pair and forget them,
+ * so that a later Socket_outInitialize does not overwrite still open descriptors.
+ */
+static void Socket_closePair(void)
+{
+	int i;
+
+	FUNC_ENTRY;
+	for (i = 0; i < 2; ++i)
+	{
+		if (sockfd[i] != INVALID_SOCKET)
+		{
+#if defined(_WIN32)
+			closesocket(sockfd[i]);
+#else
+			close(sockfd[i]);
+#endif
+			sockfd[i] = INVALID_SOCKET;
+		}
+	}
+	FUNC_EXIT;
+}
+
 /**
  * Initialize the socket module
  */
@@ -347,6 +379,7 @@
 void Socket_outTerminate(void)
 {
 	FUNC_ENTRY;
+	Socket_closePair();
 	ListFree(mod_s.connect_pending);
 	ListFree(mod_s.write_pending);
 #if defined(USE_SELECT)
```

