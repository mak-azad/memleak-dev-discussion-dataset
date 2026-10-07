# Memory leak when using pcl::visualization::PCLVisualizer with interactor

- URL: https://github.com/PointCloudLibrary/pcl/issues/2225
- Repo: PointCloudLibrary/pcl (language: C++)
- State: open; created 2018-02-22T18:10:04Z; status ok; passes main

## Issue body

reporter (NONE) · a-lerion · 2018-02-22T18:10:04Z · https://github.com/PointCloudLibrary/pcl/issues/2225

<!--- WARNING: This is an issue tracker, please use our mailing list for questions: www.pcl-users.org. -->

<!--- Provide a general summary of the issue in the Title above -->

## Your Environment
<!--- Include as many relevant details about the environment you experienced the bug in -->
I have two environments, one with Linux and the other one with Windows.
Windows environment:
* Operating System and version: Windows 7 x64 Professional
* Compiler: Microsoft Visual Studio 2017 toolset v140
* PCL Version: 1.8.0

Linux environment:
* Operating System and version: xubuntu 16.10 x64
* Compiler: g++ 5.2
* PCL Version: 1.8.0

## Context
<!--- How has this issue affected you? What are you trying to accomplish? -->
<!--- Providing context helps us come up with a solution that is most useful in the real world -->
I want to display point clouds and save them to images. I want to be able to rotate, scale and move clouds while displaying them.

## Expected Behavior
<!--- If you're describing a bug, tell us what should happen -->
<!--- If you're suggesting a change/improvement, tell us how it should work -->
Every time PCLVisualizer is created and initialized it consumes some RAM and GPU RAM. It has to be freed after calls to close and release.

## Current Behavior
<!--- If describing a bug, tell us what happens instead of the expected behavior -->
<!--- If suggesting a change/improvement, explain the difference from current behavior -->
Despite calling close on PCLVisualizer and release on a shared pointer holding it most of the allocated memory is not released.

## Code to Reproduce
<!--- Provide a link to a live example, or an unambiguous set of steps to -->
<!--- reproduce this bug. Include code to reproduce, if relevant -->

## Possible Solution
<!--- Not obligatory, but suggest a fix/reason for the bug, -->
<!--- or ideas how to implement the addition or change -->
This is definetely related to reference counting of VTK objects and a cyclic strong reference chain created in createInteractor. When interactor is not created no memory is leaked, but visualizer is not usable.

I tried to clear the reference cycle in destructor of PCLVisualizer. It worked on Windows. But on Linux I get BadWindow error in console and application terminates. I added the following to `if (interactor_ != NULL)` block of destructor

    interactor_->SetRenderWindow(nullptr);
    interactor_->SetInteractorStyle(nullptr);

Could you tell what else needs to be done so that X Server would not report an error?

## Comment 367936732

maintainer (MEMBER) · taketwo · 2018-02-23T07:58:26Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-367936732

Could you report your VTK version(s) as well? Are you using the same on Windows and Linux? This may be the reason for different behavior.

## Comment 367939179

maintainer (MEMBER) · taketwo · 2018-02-23T08:11:21Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-367939179

There seems to be an [`UnRegister`](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html#a14b7cf3e577e65102f3efba618b335f6) function in `vtkRenderWindowInteractor`, maybe relevant. Though I should say I have no idea what argument it expects. `this`? 

## Comment 368220299

reporter (NONE) · a-lerion · 2018-02-24T11:02:31Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-368220299

I use same VTK versions on both platforms. I tried VTK 7.1 and VTK 8.1

## Comment 368220477

reporter (NONE) · a-lerion · 2018-02-24T11:05:46Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-368220477

Setting style and window to nullptr that way calls Unregister for them before unsetting them inside interactor.

## Comment 368224199

maintainer (MEMBER) · taketwo · 2018-02-24T12:12:22Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-368224199

I am afraid I don't have any other suggestions. In the meantime we can `#ifdef` this fix at least for Windows. @PointCloudLibrary/maintainers  

## Comment 368231357

maintainer (MEMBER) · SergioRAgostinho · 2018-02-24T14:18:51Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-368231357

@a-lerion can you save us some time and post the code snippet you're using to verify this behavior? 

I'm not experienced enough with VTK so I'll need to dig a little bit in the mud before I can provide meaningful insights. I'm ok in pushing the quick fix as an intermediate solution. 

## Comment 368471152

reporter (NONE) · a-lerion · 2018-02-26T11:28:54Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-368471152

OK. I'll add it tonight

## Comment 368669049

reporter (NONE) · a-lerion · 2018-02-26T22:11:00Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-368669049

I used the following code with cmake to specify link and include directories. Just inputting 1 and 0 successively was enough to get a leak for me.

```C++
#include <iostream>
#include <memory>
#include <pcl/visualization/pcl_visualizer.h>
#include <vtkWindowToImageFilter.h>
#include <vtkSmartPointer.h>
#include <vtkRenderWindow.h>

void testVisualizationLib()
{
    std::shared_ptr<pcl::visualization::PCLVisualizer> visualization;
    boost::shared_ptr<pcl::PointCloud<pcl::PointXYZRGB>> points;

    for (;;)
    {
        unsigned action;
        std::cin >> action;

        switch (action)
        {
            case 1:
            {
                visualization.reset(new pcl::visualization::PCLVisualizer("", false));
                visualization->getRenderWindow()->SetOffScreenRendering(1);
                visualization->setSize(1024, 768);
                visualization->createInteractor();

                int newViewportID = 0;
                visualization->createViewPort(0.0, 0.0, 1.0, 1.0, newViewportID);

                visualization->resetCameraViewpoint();
                visualization->resetCamera();

                break;
            }
            case 0:
            {
                if (visualization)
                {
                    visualization->close();
                }
                visualization.reset();
                break;
            }
            case 2:
            {
                visualization->removeAllPointClouds();
                visualization->removeCorrespondences("text_result");
                visualization->removeAllCoordinateSystems(1);
                break;
            }
            case 3:
            {
                points.reset(new pcl::PointCloud<pcl::PointXYZRGB>());

                for (unsigned i = 0; i < 350'000; ++i)
                {
                    pcl::PointXYZRGB point;

                    point.x = std::rand() / 32767.f;
                    point.y = std::rand() / 32767.f;
                    point.z = 5 + std::rand() / 32767.f;

                    points->push_back(point);
                }
                points->width = points->size();
                points->height = 1;
                points->is_dense = true;

                visualization->addPointCloud(points, "srcInput", 1);
                visualization->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 1.8, "srcInput", 1);
                visualization->addText("Average points: 3500", 5, 20, 40, 0.6784, 1.0, 0.1843, "text_result", 1);
                break;
            }
            case 5:
            {
                visualization->spinOnce();

                vtkSmartPointer<vtkWindowToImageFilter> m_windowVisualizerToImageFilter = vtkSmartPointer<vtkWindowToImageFilter>::New();
                m_windowVisualizerToImageFilter->SetInput(visualization->getRenderWindow());
                m_windowVisualizerToImageFilter->SetInputBufferTypeToRGB();
                m_windowVisualizerToImageFilter->ReadFrontBufferOff();
                m_windowVisualizerToImageFilter->Update();
                vtkImageData* vtkRGBimage = m_windowVisualizerToImageFilter->GetOutput();
                int dimsRGBImage[3];
                vtkRGBimage->GetDimensions(dimsRGBImage);

                // Use vtkRGBimage here

                break;
            }
            case 9:
                return;
        }
    }
}

int main(int argc, char** argv)
{
    std::srand(std::time(nullptr));

    testVisualizationLib();

    return 0;
}
```

## Comment 431674700

other (NONE) · Bardo91 · 2018-10-21T14:43:52Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-431674700

I had similar issues with the visualizer that might be related. I am running a registration algorithm, and after several iterations, I got run out of memory on my computer. I dug in it a bit and using the memory leak checker from gperftools and It reported memory leaks in something called `vkgetinstanceprocaddr`. 

I will keep working on it and I will try to report as much as possible.

I am using PCL-1.8.1 with VTK-6.2 in Ubuntu 16.04.

## Comment 501281591

other (NONE) · Dysl3xik · 2019-06-12T13:48:59Z · https://github.com/PointCloudLibrary/pcl/issues/2225#issuecomment-501281591

This may be related to https://github.com/PointCloudLibrary/pcl/issues/2386 
