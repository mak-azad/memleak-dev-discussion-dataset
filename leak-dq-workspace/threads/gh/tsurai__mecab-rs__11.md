# There is a memory leak？

- URL: https://github.com/tsurai/mecab-rs/issues/11
- Repo: tsurai/mecab-rs (language: Rust)
- State: open; created 2024-12-10T01:22:22Z; status ok; passes main

## Issue body

reporter (NONE) · zurmokeeper · 2024-12-10T01:22:22Z · https://github.com/tsurai/mecab-rs/issues/11

### I wrote a node.js rust addon and the rust code uses mecab-rs to call mecab.   mecab-rs is the latest version。

### Then I see the memory of my node.js application as shown above, the part corresponding to the beginning of the peak is indeed increasing in the number of requests, but after the number of requests come down the memory usage does not drop to the previous state, it will drop, but it is still a very high position.

@tsurai @DoumanAsh 


![image](https://github.com/user-attachments/assets/68f95ed6-aba3-43be-999b-dcb4e6a8780b)



![image](https://github.com/user-attachments/assets/6277fa01-f21f-417f-a66c-4176986cc867)


my code is as follows


```
#![deny(clippy::all)]

#[macro_use]
extern crate napi_derive;
extern crate mecab;

use mecab::Tagger;
use std::vec::Vec;

#[cfg(target_pointer_width = "32")]
type CLong = i32;

#[cfg(target_pointer_width = "64")]
type CLong = i64;

#[napi(object)]
pub struct NodeInfo {
  pub id: u32,
  pub surface: String,
  pub feature: String,
  pub len: u16,
  pub rc_attr: u16,
  pub lc_attr: u16,
  pub posid: u16,
  pub char_type: u8,
  pub stat: u8,
  pub isbest: i32,
  pub alpha: f64,
  pub beta: f64,
  pub prob: f64,
  #[napi(ts_type = "number")]
  pub cost: CLong,
}

#[napi]
pub fn parse_as_node(input: String) -> Vec<NodeInfo> {
  let mut tagger = Tagger::new("");
  let my_input: &str = input.as_str(); 

  let mut result = Vec::new();
  for node in tagger.parse_to_node(my_input).iter_next() {
      let node_info = NodeInfo {
        id: node.id,
        surface: (node.surface)[..(node.length as usize)].to_string(),
        feature: node.feature.to_string(),
        len: node.length,
        rc_attr: node.rcattr,
        lc_attr: node.lcattr,
        posid: node.posid,
        char_type: node.char_type,
        stat: node.stat,
        isbest: if node.isbest { 1 } else { 0 },
        alpha: node.alpha as f64,
        beta: node.beta as f64,  
        prob: node.prob as f64,
        cost: node.cost,
    };
    result.push(node_info);
  }
  result
}

Then the method parse_as_node is called directly

```




## Comment 2529996765

other (CONTRIBUTOR) · DoumanAsh · 2024-12-10T01:32:55Z · https://github.com/tsurai/mecab-rs/issues/11#issuecomment-2529996765

It is a bit difficult to say without checking code under valgrind
Can you write simple Rust program with your example and run it under valgrind?

I do not really use mecab myself nowadays though so I'm not sure if there can be any isuses

## Comment 2530257629

reporter (NONE) · zurmokeeper · 2024-12-10T04:12:45Z · https://github.com/tsurai/mecab-rs/issues/11#issuecomment-2530257629

> valgrind

Thanks for the reply, I'll give it a try

## Comment 2537635980

reporter (NONE) · zurmokeeper · 2024-12-12T02:28:56Z · https://github.com/tsurai/mecab-rs/issues/11#issuecomment-2537635980

@DoumanAsh 

It may not be a memory leak, I just realized that this memory indicator is `WSS`, not `RES`, I went in to the pod in k8s , and used the `top` command to see that the `node's RES memory` is reclaimed normally.

I guess it's a `Mecab` problem. I looked at the mecab source code and found that it uses `mmap`, and I also observed that the `memory cache` of my pod is very high. I suspect that node.js is calling mecab via mecab-rs, and mecab is mapping files and other data directly into memory, but this part of the memory doesn't belong to mecab-rs, so I don't think it's a memory leak. belongs to `node's RES`.

So the memory of the pod is very high, but actually node.js uses very little, I don't know what you think about this?


## Comment 2537665941

other (CONTRIBUTOR) · DoumanAsh · 2024-12-12T02:38:41Z · https://github.com/tsurai/mecab-rs/issues/11#issuecomment-2537665941

As far as I remember it needs mmap to efficiently load model rather than using RAM so it makes sense
You should avoid creating multiple instances of the same Mecab instances and prefer to cache it

## Comment 2537760333

reporter (NONE) · zurmokeeper · 2024-12-12T03:59:37Z · https://github.com/tsurai/mecab-rs/issues/11#issuecomment-2537760333

@DoumanAsh 

Just one more question, I used to call mecab as a child process, it is reasonable to say that mecab is also using mmap at this time, why the memory cache is not as big as the current one, I have changed to rust addon to call mecab-rs.

After changing to rust addon to call mecab-rs, the memory cache went from 400M to 8-900M, is mecab's mmap recovery so slow?

Now I create a mecab instance every time I call it, and I'm worried that if I don't create a new mecab instance every time, I'm not going to have a memory leak.

```
impl Drop for Tagger {
    fn drop(&mut self) {
        unsafe {
            mecab_destroy(self.inner);
            self.free_input();
        }
    }
}
```

After all, there is memory release code in the rust code.

## Comment 2537826899

other (CONTRIBUTOR) · DoumanAsh · 2024-12-12T05:08:14Z · https://github.com/tsurai/mecab-rs/issues/11#issuecomment-2537826899

You should remember that it is OS who is responsible for actual management of resources
If it is done by child process, it is possible OS would keep it tied to parent process even if child process dies (in case you'll use it again)

I cannot really tell what's going on as I would need to review mecab code, but as long as there is no obvious memory leaks you should not have issues I think
