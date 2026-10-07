# free(): invalid pointer exception

- URL: https://github.com/htacg/tidy-html5/issues/1086
- Repo: htacg/tidy-html5 (language: C)
- State: open; created 2023-05-09T13:36:25Z; status ok; passes main

## Issue body

reporter (NONE) · antonfries · 2023-05-09T13:36:25Z · https://github.com/htacg/tidy-html5/issues/1086

.tidyrc content:
```
show-warnings: yes
markup: no
mute-id: yes
mute:
    INSERTING_TAG
    MISSING_DOCTYPE
    PROPRIETARY_ELEMENT
    MISSING_TITLE_ELEMENT
    MISSING_ATTRIBUTE
    MISMATCHED_ATTRIBUTE_WARN
    PROPRIETARY_ATTRIBUTE
    TAG_NOT_ALLOWED_IN
    TRIM_EMPTY_ELEMENT
    DISCARDING_UNEXPECTED
```
Execution:
```
15:33 $ HTML_TIDY=.tidyrc tidy -q sample.html
Info: messages of type "INSERTING_TAG" will not be output (STRING_MUTING_TYPE)
Info: messages of type "MISSING_DOCTYPE" will not be output (STRING_MUTING_TYPE)
Info: messages of type "PROPRIETARY_ELEMENT" will not be output (STRING_MUTING_TYPE)
Info: messages of type "MISSING_TITLE_ELEMENT" will not be output (STRING_MUTING_TYPE)
Info: messages of type "MISSING_ATTRIBUTE" will not be output (STRING_MUTING_TYPE)
Info: messages of type "MISMATCHED_ATTRIBUTE_WARN" will not be output (STRING_MUTING_TYPE)
Info: messages of type "PROPRIETARY_ATTRIBUTE" will not be output (STRING_MUTING_TYPE)
Info: messages of type "TAG_NOT_ALLOWED_IN" will not be output (STRING_MUTING_TYPE)
Info: messages of type "TRIM_EMPTY_ELEMENT" will not be output (STRING_MUTING_TYPE)
Info: messages of type "DISCARDING_UNEXPECTED" will not be output (STRING_MUTING_TYPE)
free(): invalid pointer
Aborted
```

Tried it with make install "HTML Tidy for Linux version 5.9.20" and regular apt-"5.6.0"

This only happens if there are more than 9 mute rules
