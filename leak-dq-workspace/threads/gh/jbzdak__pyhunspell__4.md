# Bugs found in pyhunspell-0.1-6.fc17 using gcc-with-cpychecker static analyzer

- URL: https://github.com/jbzdak/pyhunspell/issues/4
- Repo: jbzdak/pyhunspell (language: C)
- State: open; created 2015-04-18T13:08:43Z; status ok; passes offcwe

## Issue body

reporter (NONE) · GoogleCodeExporter · 2015-04-18T13:08:43Z · https://github.com/jbzdak/pyhunspell/issues/4

```
I originally filed this downstream in Fedora's bug tracker as 
https://bugzilla.redhat.com/show_bug.cgi?id=800116 ; filing here so that 
upstream developers can see it.

Description of problem:
I've been writing an experimental static analysis tool to detect bugs commonly
occurring within C Python extension modules:
  https://fedorahosted.org/gcc-python-plugin/
  http://gcc-python-plugin.readthedocs.org/en/latest/cpychecker.html
  http://fedoraproject.org/wiki/Features/StaticAnalysisOfPythonRefcounts

I ran the latest version of the tool (in git master; post 0.9) on
pyhunspell-0.1-6.fc17.src.rpm, and it reports various errors.

You can see a list of errors here, triaged into categories (from most
significant to least significant):
http://fedorapeople.org/~dmalcolm/gcc-python-plugin/2012-03-05/pyhunspell-0.1-6.
fc17/

I've manually reviewed the issues reported by the tool.

Within the category "Reference leaks" the 4 issues reported appear to be
genuine  memory leaks, each of the form:
   PyList_Append(list, Py_BuildValue())
When Py_BuildValue() succeeds it returns a new reference, but PyList_Append
doesn't steal that reference, it adds a new reference.  Hence this leaks a
reference to the built value, and it becomes "immortal" for the rest of the
lifetime of the process.

Within the category "Segfaults within error-handling paths" the 4 issues
reported are for the same code as the above, considering the case where the
PyList_New() call fails (e.g. due to out of memory), it will return NULL, and
then the PyList_Append(NULL, item) call will segfault.  Note that the
Py_BuildValue() and PyList_Append calls could also fail.

Suggested fix is to add an intermediate value, changing the calls to:

    slist_list = PyList_New(0);
    if (!slist_list) {
        return NULL;
    }

within the loop:
    PyObject *item; 
    item = Py_BuildValue(etc);
    if (!item) {
        Py_DECREF(slist_list);
        return NULL;
    }
    if (-1 == PyList_Append(slist_list, item)) {
        Py_DECREF(slist_list);
        Py_DECREF(item);
        return NULL;
    }
    Py_DECREF(item);

or similar.

There may of course be other bugs in my checker tool.

Hope this is helpful; let me know if you need help reading the logs that the
tool generates - I know that it could use some improvement.

Version-Release number of selected component (if applicable):
pyhunspell-0.1-6.fc17
gcc-python-plugin post-0.9 git 11462291a66c8db693c8884cb84b795bb5988ffb running
the checker in an *f16* chroot



```

Original issue reported on code.google.com by `3583byte...@gmail.com` on 21 Mar 2012 at 6:53

