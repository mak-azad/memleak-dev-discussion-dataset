# Pango attributeWriteKlass wants a `Ptr AttrClass` instead of `Maybe AttrClass`

- URL: https://github.com/haskell-gi/haskell-gi/issues/23
- Repo: haskell-gi/haskell-gi (language: Haskell)
- State: open; created 2016-05-06T04:35:17Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · hamishmack · 2016-05-06T04:35:17Z · https://github.com/haskell-gi/haskell-gi/issues/23

In file `bindings/Pango/GI/Structs/Attribute.hs` the read and write functions for the `class` attribute of Pango `Attribute` struct looks like this:

```
attributeReadKlass :: MonadIO m => Attribute -> m (Maybe AttrClass)
attributeReadKlass s = liftIO $ withManagedPtr s $ \ptr -> do
    val <- peek (ptr `plusPtr` 0) :: IO (Ptr AttrClass)
    result <- convertIfNonNull val $ \val' -> do
        val'' <- (newPtr 32 AttrClass) val'
        return val''
    return result

attributeWriteKlass :: MonadIO m => Attribute -> Ptr AttrClass -> m ()
attributeWriteKlass s val = liftIO $ withManagedPtr s $ \ptr -> do
    poke (ptr `plusPtr` 0) (val :: Ptr AttrClass)
```

Should attributeWriteKlass take a `Maybe AttrClass` instead of a `Ptr AttrClass`?


## Comment 217804293

maintainer (COLLABORATOR) · garetxe · 2016-05-09T08:23:18Z · https://github.com/haskell-gi/haskell-gi/issues/23#issuecomment-217804293

This is on purpose (although I am definitely open to changing it if we can come up with a better way of doing things). The issue here is memory ownership: if you pass in `Just k` to `attributeWriteKlass`, who is responsible for freeing the memory? The block of memory inside a `Pango.AttrClass` will be freed by the haskell GC at some point, so we cannot just copy the pointer to the memory itself.

We could instead make a copy, and write a copy to that, but that will probably give rise to a memory leak eventually.

So what we do right now is leaving the responsibility of doing things right to the caller. Not ideal, but there is not enough info to do things safely at binding generation time, as far as I can see.

`attributeReadKlass` has some of the same issues in principle, so perhaps it would be better to also just return a pointer  (also to remove the asymmetry between `Read` and `Write`).

I am honestly not sure what is the best thing to do here. Any preferences/suggestions?


## Comment 218142904

reporter (COLLABORATOR) · hamishmack · 2016-05-10T12:30:34Z · https://github.com/haskell-gi/haskell-gi/issues/23#issuecomment-218142904

I have created issue #24 to track the problem I was actually trying to solve when I came across this.  I think the pango attribute stuff is a bit broken in GIR.  I'm not sure if it should even be possible to write to the `Attribute.class` since doing so would be transforming the attribute from one subtype to another.  The correct way to set the subtype would seem to be suing functions like `pango_attr_font_desc_new` to allocate the structure and set the subtype.

We should probably make `Attribute.class` read only.

As for the `AttrClass` type, these should probably only me constructed by pango and we don't have to worry about scope as they are global.  They are allocated as static locals in the `pang_attr_*_new` functions, like this:

```
PangoAttribute *
pango_attr_font_desc_new (const PangoFontDescription *desc)
{
  static const PangoAttrClass klass = {
    PANGO_ATTR_FONT_DESC,
    pango_attr_font_desc_copy,
    pango_attr_font_desc_destroy,
    pango_attr_font_desc_equal
  };

  PangoAttrFontDesc *result = g_slice_new (PangoAttrFontDesc);
  pango_attribute_init (&result->attr, &klass);
  result->desc = pango_font_description_copy (desc);

  return (PangoAttribute *)result;
}
```

