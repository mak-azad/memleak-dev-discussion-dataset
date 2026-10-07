# exit - free(): invalid pointer

- URL: https://github.com/akhellad/Minishell/issues/6
- Repo: akhellad/Minishell (language: C)
- State: open; created 2023-08-04T00:00:50Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · unkn0wn107 · 2023-08-04T00:00:50Z · https://github.com/akhellad/Minishell/issues/6

```
minishell> exit
free(): invalid pointer
Aborted (core dumped)
```

ça ne corrige pas le problème :
```
if (infos->old_pwd)
     free(infos->old_pwd);
```

C'est donc que old_pwd n'est pas NULL mais a certainement une adresse invalide, probablement du à un mauvais retour de `ft_substr()`  L40 de main.c : 
```
if (!ft_strncmp(infos->envp[i], "OLDPWD=", 7))
	infos->old_pwd = ft_substr(infos->envp[i],
			7, ft_strlen(infos->envp[i]) - 7);
```


## Comment 1677933447

maintainer (OWNER) · akhellad · 2023-08-14T19:25:11Z · https://github.com/akhellad/Minishell/issues/6#issuecomment-1677933447

je n'ai pas encore pull ton travail mais sur mon minishell le exit fonctionne bien, je te redis ca quand j'ai finis d'observer tous ca
