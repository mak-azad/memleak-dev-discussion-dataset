# ft_lstdelone

- URL: https://github.com/nz-nz/Libft/issues/54
- Repo: nz-nz/Libft (language: C)
- State: open; created 2019-06-29T17:49:30Z; status ok; passes main

## Issue body

reporter (OWNER) · nz-nz · 2019-06-29T17:49:30Z · https://github.com/nz-nz/Libft/issues/54


 
--
Prototype | void ft_lstdelone(t_list**alst,void(*del)(void *, size_t));
Description | Takes as a parameter a link’s pointer address and frees the memory of the link’s content using the function del given as a parameter, then frees the link’s memory using free(3). The memory of next must not be freed under any circumstance. Finally, the pointer to the link that was just freed must be set to NULL (quite similar to the function ft_memdel in the mandatory part).
Param. #1 | The adress of a pointer to a link that needs to be freed.
Return value | None.
Libc functions | free(3)


