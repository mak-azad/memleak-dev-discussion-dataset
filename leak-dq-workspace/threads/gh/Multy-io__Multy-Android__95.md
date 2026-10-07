# JNI local reference leak in makeTransaction nested loops

- URL: https://github.com/Multy-io/Multy-Android/issues/95
- Repo: Multy-io/Multy-Android (language: Java)
- State: open; created 2026-09-21T12:07:51Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-21T12:07:51Z · https://github.com/Multy-io/Multy-Android/issues/95

## Summary

`makeTransaction` in `app/src/main/cpp/scratch.cpp` creates JNI local references inside nested loops and never calls `DeleteLocalRef`. A Bitcoin send with many addresses / UTXOs can overflow the JNI local reference table (~512 slots) and abort the process (`JNI ERROR: local reference table overflow`).

Called from `NativeDataHelper.makeTransaction` and `estimateTransactionFee`.

## Code

Outer loop (per address) — four array refs per iteration, overwritten without delete:

```cpp
for (int i = 0; i < length; i++) {
    env->CallVoidMethod(jObjectTransaction, jMidSetup, addressId);
    jintArray outIds = (jintArray) env->CallObjectMethod(jObjectTransaction, jMidIds);
    jobjectArray hashes = (jobjectArray) env->CallObjectMethod(jObjectTransaction, jMidHashes);
    jobjectArray keys = (jobjectArray) env->CallObjectMethod(jObjectTransaction, jMidKeys);
    jobjectArray amounts = (jobjectArray) env->CallObjectMethod(jObjectTransaction, jMidAmounts);

Inner loop (per UTXO) — three jstring refs per iteration:

for (int k = 0; k < stringCount; k++) {
    jstring jHash = (jstring) env->GetObjectArrayElement(hashes, k);
    jstring jKey = (jstring) env->GetObjectArrayElement(keys, k);
    jstring jAmount = (jstring) env->GetObjectArrayElement(amounts, k);
    JniString hashString(env, jHash);
    // ...
}

JniString only calls ReleaseStringUTFChars; it does not DeleteLocalRef the jstring. Peak usage is about length × (4 + 3 × UTXOs per address) until the JNI method returns.

How to trigger
1. Enable CheckJNI: adb shell setprop debug.checkjni 1, then restart the app.
2. Build a send (or fee estimate) that uses many UTXOs, enough that addresses × UTXOs pushes local refs past ~512 (e.g. tens of addresses with many small outputs).
3. Watch logcat during makeTransaction / estimateTransactionFee.

Expected
Delete each local ref after use (or wrap the loops with PushLocalFrame / PopLocalFrame).

Suggested fix
// inner loop, after JniString / use
env->DeleteLocalRef(jHash);
env->DeleteLocalRef(jKey);
env->DeleteLocalRef(jAmount);

// outer loop, after ReleaseIntArrayElements
env->DeleteLocalRef(outIds);
env->DeleteLocalRef(hashes);
env->DeleteLocalRef(keys);
env->DeleteLocalRef(amounts);

Also delete jTransaction, jObjectTransaction, and addrIds before returning.


