# Memory Leak

- URL: https://github.com/P-H-C/phc-winner-argon2/issues/257
- Repo: P-H-C/phc-winner-argon2 (language: C)
- State: open; created 2018-07-03T13:11:01Z; status ok; passes main

## Issue body

reporter (NONE) · ErikPartridge · 2018-07-03T13:11:01Z · https://github.com/P-H-C/phc-winner-argon2/issues/257

Having run the code through Valgrind and Facebook's Infer, seem to have come across a memory leak, where the value of `ctx.out` is not free'd in some circumstances.

Here's the full output of running Infer over the problematic function.
```cpp
external/argon2/src/argon2.c:289: error: MEMORY_LEAK
  memory dynamically allocated by call to `malloc()` at line 280, column 15 is not reachable after line 289, column 11.
Showing all 17 steps of the trace


external/argon2/src/argon2.c:249:1: start of procedure argon2_verify()
247.   }
248.   
249. > int argon2_verify(const char *encoded, const void *pwd, const size_t pwdlen,
250.                     argon2_type type) {
251.   

external/argon2/src/argon2.c:253:5: 
251.   
252.       argon2_context ctx;
253. >     uint8_t *desired_result = NULL;
254.   
255.       int ret = ARGON2_OK;

external/argon2/src/argon2.c:255:5: 
253.       uint8_t *desired_result = NULL;
254.   
255. >     int ret = ARGON2_OK;
256.   
257.       size_t encoded_len;

external/argon2/src/argon2.c:260:9: Taking false branch
258.       uint32_t max_field_len;
259.   
260.       if (pwdlen > ARGON2_MAX_PWD_LENGTH) {
               ^
261.           return ARGON2_PWD_TOO_LONG;
262.       }

external/argon2/src/argon2.c:264:9: Taking false branch
262.       }
263.   
264.       if (encoded == NULL) {
               ^
265.           return ARGON2_DECODING_FAIL;
266.       }

external/argon2/src/argon2.c:268:5: 
266.       }
267.   
268. >     encoded_len = strlen(encoded);
269.       if (encoded_len > UINT32_MAX) {
270.           return ARGON2_DECODING_FAIL;

external/argon2/src/argon2.c:269:9: Taking false branch
267.   
268.       encoded_len = strlen(encoded);
269.       if (encoded_len > UINT32_MAX) {
               ^
270.           return ARGON2_DECODING_FAIL;
271.       }

external/argon2/src/argon2.c:274:5: 
272.   
273.       /* No field can be longer than the encoded length */
274. >     max_field_len = (uint32_t)encoded_len;
275.   
276.       ctx.saltlen = max_field_len;

external/argon2/src/argon2.c:276:5: 
274.       max_field_len = (uint32_t)encoded_len;
275.   
276. >     ctx.saltlen = max_field_len;
277.       ctx.outlen = max_field_len;
278.   

external/argon2/src/argon2.c:277:5: 
275.   
276.       ctx.saltlen = max_field_len;
277. >     ctx.outlen = max_field_len;
278.   
279.       ctx.salt = malloc(ctx.saltlen);

external/argon2/src/argon2.c:279:5: 
277.       ctx.outlen = max_field_len;
278.   
279. >     ctx.salt = malloc(ctx.saltlen);
280.       ctx.out = malloc(ctx.outlen);
281.       if (!ctx.salt || !ctx.out) {

external/argon2/src/argon2.c:280:5: 
278.   
279.       ctx.salt = malloc(ctx.saltlen);
280. >     ctx.out = malloc(ctx.outlen);
281.       if (!ctx.salt || !ctx.out) {
282.           ret = ARGON2_MEMORY_ALLOCATION_ERROR;

external/argon2/src/argon2.c:281:10: Taking false branch
279.       ctx.salt = malloc(ctx.saltlen);
280.       ctx.out = malloc(ctx.outlen);
281.       if (!ctx.salt || !ctx.out) {
                ^
282.           ret = ARGON2_MEMORY_ALLOCATION_ERROR;
283.           goto fail;

external/argon2/src/argon2.c:281:23: Taking false branch
279.       ctx.salt = malloc(ctx.saltlen);
280.       ctx.out = malloc(ctx.outlen);
281.       if (!ctx.salt || !ctx.out) {
                             ^
282.           ret = ARGON2_MEMORY_ALLOCATION_ERROR;
283.           goto fail;

external/argon2/src/argon2.c:286:5: 
284.       }
285.   
286. >     ctx.pwd = (uint8_t *)pwd;
287.       ctx.pwdlen = (uint32_t)pwdlen;
288.   

external/argon2/src/argon2.c:287:5: 
285.   
286.       ctx.pwd = (uint8_t *)pwd;
287. >     ctx.pwdlen = (uint32_t)pwdlen;
288.   
289.       ret = decode_string(&ctx, encoded, type);

external/argon2/src/argon2.c:289:5: Skipping decode_string(): empty list of specs
287.       ctx.pwdlen = (uint32_t)pwdlen;
288.   
289.       ret = decode_string(&ctx, encoded, type);
           ^
290.       if (ret != ARGON2_OK) {
291.           goto fail;
```

## Comment 402156334

other (CONTRIBUTOR) · WOnder93 · 2018-07-03T13:25:39Z · https://github.com/P-H-C/phc-winner-argon2/issues/257#issuecomment-402156334

Are you sure this is not a false positive? `decode_string()` does not overwrite the value of ctx.out, as far as I can tell. It can overwrite the contents of the allocated memory, but it should be still reachable when the function returns.

## Comment 402157211

reporter (NONE) · ErikPartridge · 2018-07-03T13:28:31Z · https://github.com/P-H-C/phc-winner-argon2/issues/257#issuecomment-402157211

That's what I thought too, so I isolated the code best I could in Valgrind and ran it. The code running the function otherwise lost 0 bytes, but when that function was called, 7,680 bytes were lost, which makes me believe Infer was correct.

## Comment 402214094

reporter (NONE) · ErikPartridge · 2018-07-03T16:20:17Z · https://github.com/P-H-C/phc-winner-argon2/issues/257#issuecomment-402214094

Update: ran this through cppcheck as well, which agrees it's a memory leak.

## Comment 402443052

other (CONTRIBUTOR) · WOnder93 · 2018-07-04T10:51:10Z · https://github.com/P-H-C/phc-winner-argon2/issues/257#issuecomment-402443052

Hm, that's weird... when I run `echo test | valgrind ./argon2 saltsalt` (which calls `argon2_verify()` internally), I don't get any leak. Could you please post the exact code you ran under valgrind? You say you 'isolated the code', so I'm wondering what exactly that means.

## Comment 402554254

reporter (NONE) · ErikPartridge · 2018-07-04T20:25:12Z · https://github.com/P-H-C/phc-winner-argon2/issues/257#issuecomment-402554254

```cpp
    const char *value = pwd.c_str();

    //Get a salt from /dev/urandom
    uint8_t salt[SALTLEN];
    int fd = open("/dev/urandom", O_RDONLY);
    ssize_t size = read(fd, salt, sizeof salt);
    if ( size != sizeof salt ) {
        throw "Could not generate salt";
    }
    close(fd);

    unsigned long pwdlen = strlen(value);
    char encoded[97];

    argon2i_hash_encoded(T_COST, M_COST, PARALLELISM, value, pwdlen, salt, SALTLEN, HASHLEN, encoded, 97);
    std::string res = encode;
    
    return res;
```

I tried to wrap it with as minimal code as possible, then separately analyzed that code without the argon2 code attached to ensure it was correct.

## Comment 404157149

other (CONTRIBUTOR) · sneves · 2018-07-11T12:49:53Z · https://github.com/P-H-C/phc-winner-argon2/issues/257#issuecomment-404157149

Under which parameters is this reproducible? Does it happen when `PARALLELISM=1`?

## Comment 404669233

other (CONTRIBUTOR) · technion · 2018-07-12T22:22:31Z · https://github.com/P-H-C/phc-winner-argon2/issues/257#issuecomment-404669233

I found a legitimate issue previously with Infer, but when I hit this this issue I eventually concluded it was an FP. I actually logged this with Infer:

https://github.com/facebook/infer/issues/493

They appeared to agree, of course, there's room for something subtle to be hanging around.

