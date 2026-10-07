# CNTK and GPU memory leaking

- URL: https://github.com/microsoft/CNTK/issues/3778
- Repo: microsoft/CNTK (language: C++)
- State: open; created 2019-11-30T03:31:30Z; status ok; passes offcwe

## Issue body

reporter (NONE) · yelandgit · 2019-11-30T03:31:30Z · https://github.com/microsoft/CNTK/issues/3778

I am trying to work with autoencoder. I build first one. I extract encoder, and calculate new data for next autoencoder.

`z1 = C.Function.load("./NTIMIT/ae-1240-2000-1240.dnn")    # gpu = 191 Mb`
`z1e = GetEncoder(None, z1, C.sigmoid)                                # gpu = 275 Mb`
`dset = z1e.eval(dataset)                                                         # gpu =  3931 Mb`
`tset = z1e.eval(testset)                                                           # gpu = 3931 Mb`

What do I see? I see 4Gb GPU memory in use when I've recieved my dset/tset. I don't understand why it happened. Why 4 Gb? My data set has much smaller size. Why GPU memory still in use after calculation? Why CNTK doesn't release used GPU memory?

Again, why 4 Gb? My data set sizes:
dataset = 600 Mb
testset = 200 Mb
dset = 990 Mb
tset = 330 Mb

The 1st autoencoder is 1240+2000+1240 (20 Mb)
The 2nd autoencoder is 2000+2000+2000 (32 Mb)

When I create new autoencoder and train one, I got 8Gb GPU memory in use (old 4Gb + new 4Gb). Plus at the end I didn't save network because "RuntimeError: CUDA failure 2: out of memory".  Same error I got at first training step with minibatch size 30% from whole dataset. After reducing minibatch size to 10% I could make something without ability to save result

This is serious GPU memory leak in CNTK

RTX 2080 Ti 11Gb
CUDA 10.1.243
CNTK 2.7
python 3.6.8
Linux Mint 19.2 Tina


## Comment 560328794

other (NONE) · haixpham · 2019-12-02T10:14:55Z · https://github.com/microsoft/CNTK/issues/3778#issuecomment-560328794

Can you please elaborate:
- How many parameters are there in your network?
- How many samples in each batch, and their size?

I have used CNTK extensively for large GAN-type networks and see no problem.

## Comment 560755672

reporter (NONE) · yelandgit · 2019-12-02T22:27:22Z · https://github.com/microsoft/CNTK/issues/3778#issuecomment-560755672

All answers for your questions in my previous post.

How I see today my problem is not released GPU memory after eval(). Do you see the code and comments in my 1st post? Do you see how used GPU memory is changed after each step? And see data amount bottom. The data set has 600 Mb + network has 20 Mb, but for evaluation allocated GPU memory is 4 Gb. Plus after evaluation GPU memory is not released. What the fu... dge?
