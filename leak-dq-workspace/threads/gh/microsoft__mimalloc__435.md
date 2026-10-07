# IOS crash --- "pointer being freed was not allocated"

- URL: https://github.com/microsoft/mimalloc/issues/435
- Repo: microsoft/mimalloc (language: C)
- State: open; created 2021-07-05T09:11:35Z; status ok; passes main

## Issue body

reporter (NONE) · gaxlin · 2021-07-05T09:11:35Z · https://github.com/microsoft/mimalloc/issues/435


![image](https://user-images.githubusercontent.com/1112308/124447160-b0cc5e00-ddb3-11eb-87b4-325853d13ecf.png)

malloc: *** error for object 0x106890000: pointer being freed was not allocated
(3874,0x103cfb880) malloc: *** set a breakpoint in malloc_error_break to debug

but it would be ok if I do not link the mimalloc 

## Comment 873949255

reporter (NONE) · gaxlin · 2021-07-05T09:15:03Z · https://github.com/microsoft/mimalloc/issues/435#issuecomment-873949255

what i use here is just some stl string operation, return a string

## Comment 873951535

reporter (NONE) · gaxlin · 2021-07-05T09:17:37Z · https://github.com/microsoft/mimalloc/issues/435#issuecomment-873951535


std::string get_file_path()
{
	return str_format(get_dir(true) + "/data.conf");
}
