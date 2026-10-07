# ft_lstdelone

- URL: https://github.com/luanldcarvalho/42/issues/40
- Repo: luanldcarvalho/42 (language: C)
- State: open; created 2021-10-04T15:37:39Z; status ok; passes main

## Issue body

reporter (OWNER) · luanldcarvalho · 2021-10-04T15:37:39Z · https://github.com/luanldcarvalho/42/issues/40

## ft_lstdelone
|Prototype|
|---|
|void ft_lstdelone(t_list *lst, void (*del)(void
*));|

|Parameters|
|---|
|#1. The element to free.|
|#2. The address of the function used to delete the content.|

|Return value|
|---|
|None|

|External functs|
|---|
|free|

|Description|
|---|
|Takes as a parameter an element and frees the memory of the element’s content using the function ’del’ given as a parameter and free the element. The memory of ’next’ must not be freed.|

