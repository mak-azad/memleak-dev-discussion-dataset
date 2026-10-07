# Alloc-dealloc mismatch in DOMParser::ProcessNode

- URL: https://github.com/bitmovin/libdash/issues/32
- Repo: bitmovin/libdash (language: C)
- State: open; created 2021-01-28T12:02:13Z; status ok; passes main

## Issue body

reporter (NONE) · anatols · 2021-01-28T12:02:13Z · https://github.com/bitmovin/libdash/issues/32

In DOMParser::ProcessNode a string returned from xmlTextReaderReadString is freed by delete operator. It should be done with xmlFree.

I'm not going to contribute a fix via a pull request because you require signing a CLA, which I believe is against the spirit of open source. Here's a patch though, you can apply it yourselves if you want:
```
--- source/xml/DOMParser.cpp
+++ source/xml/DOMParser.cpp
@@ -113,14 +113,14 @@ Node*   DOMParser::ProcessNode              ()
         return node;
     } else if (type == Text)
     {
-       const char* text = (const char *) xmlTextReaderReadString(this->reader);
+        xmlChar *text = xmlTextReaderReadString(this->reader);
 
        if(text != NULL)
        {
            Node *node = new Node();
            node->SetType(type);
-           node->SetText(text);
-           delete text;
+           node->SetText((const char *)text);
+           xmlFree(text);
            return node;
        }
     }
```
