# malloc(): corrupted top size

- URL: https://github.com/lvntky/nexus.c/issues/2
- Repo: lvntky/nexus.c (language: C)
- State: open; created 2024-08-22T04:16:35Z; status ok; passes offcwe

## Issue body

reporter (NONE) · yuppox · 2024-08-22T04:16:35Z · https://github.com/lvntky/nexus.c/issues/2

I tried using `wget` to get `index.html` and the server exited with the error:
```
malloc(): corrupted top size
```

If I don't pass anything in the path of the URL, it works.


## Comment 2303866163

maintainer (OWNER) · lvntky · 2024-08-22T06:15:12Z · https://github.com/lvntky/nexus.c/issues/2#issuecomment-2303866163

That's interesting, Thank you for reporting @yuppox . I think we can fix this with updating the get request handler. I can assign it to if you are interested.
