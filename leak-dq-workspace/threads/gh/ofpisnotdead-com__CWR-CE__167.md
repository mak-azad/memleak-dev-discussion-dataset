# Tree and bush textures misaligned.

- URL: https://github.com/ofpisnotdead-com/CWR-CE/issues/167
- Repo: ofpisnotdead-com/CWR-CE (language: C++)
- State: open; created 2026-07-26T14:36:50Z; status ok; passes offcwe

## Issue body

reporter (NONE) · jyetcv · 2026-07-26T14:36:50Z · https://github.com/ofpisnotdead-com/CWR-CE/issues/167

I have noticed floating pieces of textures around bushes and trees. I am guessing this is some offset issue, maybe due to the difference in how these are calculated in the new renderer. Maybe a clamping or off by one error?

<img width="1024" height="768" alt="Image" src="https://github.com/user-attachments/assets/18307156-ebeb-4ba8-acde-8d0ac0cc7c64" />

Above is Remastered where the error is prominent.

<img width="1280" height="960" alt="Image" src="https://github.com/user-attachments/assets/0e9f063d-622d-46a3-9bcf-7aa061d50f47" />

Above is Operation Flashpoint: Cold War Crisis 1.46, same scene.



## Comment 5110405420

reporter (NONE) · jyetcv · 2026-07-28T22:37:32Z · https://github.com/ofpisnotdead-com/CWR-CE/issues/167#issuecomment-5110405420

Upon further inspection, this is an issue introduced in 1.99.

## Comment 5110500832

other (CONTRIBUTOR) · simi · 2026-07-28T22:49:58Z · https://github.com/ofpisnotdead-com/CWR-CE/issues/167#issuecomment-5110500832

@jyetcv good, thanks for confirming. Definitely still worth to fix IMHO.

## Comment 5121290937

other (NONE) · lowercase-t · 2026-07-29T17:26:56Z · https://github.com/ofpisnotdead-com/CWR-CE/issues/167#issuecomment-5121290937

This is not a regression introduced in 1.99, the bug is present in Direct3D on 1.46 and 1.96 as well, and I suspect it was always present in OFP:
1.46 D3D:
<img width="1280" height="960" alt="Image" src="https://github.com/user-attachments/assets/7082c629-11e3-43ff-a0ab-5cc2e1aab402" />
1.96 D3D:
<img width="1280" height="960" alt="Image" src="https://github.com/user-attachments/assets/55a656c5-3a8e-465a-a031-975f2d637149" />

What's interesting is that it doesn't seem to be a problem when running the old old old Glide API:
1.46 Glide:
<img width="1280" height="1024" alt="Image" src="https://github.com/user-attachments/assets/7c0681aa-c1ba-4653-95af-04cb45bb92e4" />

Test mission:
```
version=11;
class Mission
{
        addOns[]={};
        randomSeed=6937091;
        class Intel
        {
        };
        class Groups
        {
                items=1;
                class Item0
                {
                        side="WEST";
                        class Vehicles
                        {
                                items=1;
                                class Item0
                                {
                                        position[]={4944.869629,159.029999,6911.407715};
                                        azimut=330.000000;
                                        id=0;
                                        side="WEST";
                                        vehicle="SoldierWB";
                                        player="PLAYER COMMANDER";
                                        leader=1;
                                        skill=0.600000;
                                        markers[]={};
                                };
                        };
                };
        };
};
class Intro
{
        addOns[]={};
        randomSeed=1559555;
        class Intel
        {
        };
};
class OutroWin
{
        addOns[]={};
        randomSeed=9168899;
        class Intel
        {
        };
};
class OutroLoose
{
        addOns[]={};
        randomSeed=7091715;
        class Intel
        {
        };
};
```

If I remember correctly (and it's been 30 years so don't trust me), Glide addressed textures the same way as OpenGL does... But DirectX had a 0.5 pixel offset. It might be a red herring, but having the pixels from bottom of the texture leak to the top by 0.5 might cause this one line of opaque pixels.

## Comment 5122133681

reporter (NONE) · jyetcv · 2026-07-29T18:45:56Z · https://github.com/ofpisnotdead-com/CWR-CE/issues/167#issuecomment-5122133681

Interesting. When I run either 1.46 and 1.96 in regular Direct3D mode, I do not see the texture offset. But when I run them in Direct3D HW T&L, then I do see it.
But in 1.99 I always see the issue regardless if Hardware T&L is enabled or disabled.

## Comment 5122545000

other (NONE) · lowercase-t · 2026-07-29T19:27:41Z · https://github.com/ofpisnotdead-com/CWR-CE/issues/167#issuecomment-5122545000

I just re-tested and I can confirm that; in the previous comment I only tried with HW T&L enabled. I get the same results as you.

## Comment 5133570957

other (CONTRIBUTOR) · simi · 2026-07-30T16:31:10Z · https://github.com/ofpisnotdead-com/CWR-CE/issues/167#issuecomment-5133570957

@lowercase-t 0.5 drift should be handled properly (I was aware of that one during OpenGL porting). 🙏 
