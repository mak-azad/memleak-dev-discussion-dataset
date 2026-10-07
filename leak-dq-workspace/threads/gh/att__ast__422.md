# ksh93: file descriptor leak

- URL: https://github.com/att/ast/issues/422
- Repo: att/ast (language: C)
- State: open; created 2018-02-22T23:51:06Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · McDutchie · 2018-02-22T23:51:06Z · https://github.com/att/ast/issues/422

Reproducing this [report from the ast-developers list](http://narkive.com/an8Y04rb.1) here as it does not appear to be fixed in current git.

There is a file descriptor leak related to process substitution in ksh. This test script by Jeff Frontz shows the list of open files grows by one on every iteration. Executing the same script on bash or zsh does not show any growth of open files.

````
#! /bin/ksh

fdUser() {
	:
}

while true
do
	fdUser <(
		echo " -e"
	)

	if [ -d /proc ]
	then
		ls /proc/$$/fd
	else
		lsof -p $$ | wc -l
	fi
	sleep 1
done
````



## Comment 504812052

other (CONTRIBUTOR) · krader1961 · 2019-06-24T01:57:35Z · https://github.com/att/ast/issues/422#issuecomment-504812052

Note that this bug exists in the ksh93u+ release as well as the current git master branch; i.e., we haven't inadvertently fixed this.

## Comment 505710708

other (CONTRIBUTOR) · krader1961 · 2019-06-26T04:14:55Z · https://github.com/att/ast/issues/422#issuecomment-505710708

LGTM modulo possibly reverting some `if ()` blocks to their earlier single-line form but that is entirely optional.

## Comment 505790309

other (CONTRIBUTOR) · siteshwar · 2019-06-26T09:09:08Z · https://github.com/att/ast/issues/422#issuecomment-505790309

@krader1961 Was this comment meant for #1338 ?

## Comment 506096822

other (CONTRIBUTOR) · krader1961 · 2019-06-27T00:56:03Z · https://github.com/att/ast/issues/422#issuecomment-506096822

> Was this comment meant for #1338 ?

Oops, yes.
