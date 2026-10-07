# attempting free on address which was not malloc()-ed in lma_kinematics_plugin

- URL: https://github.com/moveit/moveit/issues/2069
- Repo: moveit/moveit (language: C++)
- State: open; created 2020-05-08T06:26:33Z; status ok; passes main

## Issue body

reporter (MEMBER) · tylerjw · 2020-05-08T06:26:33Z · https://github.com/moveit/moveit/issues/2069

Found using this PR: #2057

Debug output from travis run:

```C++
=================================================================
==8122==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x613000014cd0 in thread T0
    #0 0x7f4690c0e7a8 in __interceptor_free (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xde7a8)
    #1 0x7f467970cef1 in KDL::ChainIkSolverPos_LMA::~ChainIkSolverPos_LMA() (/opt/ros/melodic/lib/liborocos-kdl.so.1.4+0x39ef1)
    #2 0x7f4679b8dcc3 in lma_kinematics_plugin::LMAKinematicsPlugin::searchPositionIK(geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, double, std::vector<double, std::allocator<double> > const&, std::vector<double, std::allocator<double> >&, boost::function<void (geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&)> const&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&, kinematics::KinematicsQueryOptions const&) const (/root/ros_ws/devel/.private/moveit_kinematics/lib//libmoveit_lma_kinematics_plugin.so+0x1ccc3)
    #3 0x7f4679b7d2ec in lma_kinematics_plugin::LMAKinematicsPlugin::searchPositionIK(geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, double, std::vector<double, std::allocator<double> > const&, std::vector<double, std::allocator<double> >&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&, kinematics::KinematicsQueryOptions const&) const (/root/ros_ws/devel/.private/moveit_kinematics/lib//libmoveit_lma_kinematics_plugin.so+0xc2ec)
    #4 0x56254aefcac1 in KinematicsTest_randomWalkIK_Test::TestBody() (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x3aac1)
    #5 0x7f469090231e in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0xa031e)
    #6 0x7f46908c99b5 in testing::Test::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x679b5)
    #7 0x7f46908c9e18 in testing::TestInfo::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x67e18)
    #8 0x7f46908ca494 in testing::TestCase::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x68494)
    #9 0x7f46908cee05 in testing::internal::UnitTestImpl::RunAllTests() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x6ce05)
    #10 0x7f46908cf3f7 in testing::UnitTest::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x6d3f7)
    #11 0x56254aee8edc in main (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x26edc)
    #12 0x7f468d27eb96 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21b96)
    #13 0x56254aee91a9 in _start (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x271a9)
0x613000014cd0 is located 16 bytes inside of 352-byte region [0x613000014cc0,0x613000014e20)
allocated by thread T0 here:
    #0 0x7f4690c0eb40 in __interceptor_malloc (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xdeb40)
    #1 0x7f46903ed5ec in Eigen::internal::aligned_malloc(unsigned long) (/root/ros_ws/install/lib/libmoveit_robot_model.so.1.0.1+0x1145ec)
SUMMARY: AddressSanitizer: bad-free (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xde7a8) in __interceptor_free
==8122==ABORTING
=================================================================
==8292==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x61300001b090 in thread T0
    #0 0x7fe383d4c7a8 in __interceptor_free (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xde7a8)
    #1 0x7fe36c80cef1 in KDL::ChainIkSolverPos_LMA::~ChainIkSolverPos_LMA() (/opt/ros/melodic/lib/liborocos-kdl.so.1.4+0x39ef1)
    #2 0x7fe36cc8dcc3 in lma_kinematics_plugin::LMAKinematicsPlugin::searchPositionIK(geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, double, std::vector<double, std::allocator<double> > const&, std::vector<double, std::allocator<double> >&, boost::function<void (geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&)> const&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&, kinematics::KinematicsQueryOptions const&) const (/root/ros_ws/devel/.private/moveit_kinematics/lib//libmoveit_lma_kinematics_plugin.so+0x1ccc3)
    #3 0x7fe36cc7d2ec in lma_kinematics_plugin::LMAKinematicsPlugin::searchPositionIK(geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, double, std::vector<double, std::allocator<double> > const&, std::vector<double, std::allocator<double> >&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&, kinematics::KinematicsQueryOptions const&) const (/root/ros_ws/devel/.private/moveit_kinematics/lib//libmoveit_lma_kinematics_plugin.so+0xc2ec)
    #4 0x55eec3aa6ad5 in KinematicsTest_unitIK_Test::TestBody() (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x42ad5)
    #5 0x7fe383a4031e in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0xa031e)
    #6 0x7fe383a079b5 in testing::Test::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x679b5)
    #7 0x7fe383a07e18 in testing::TestInfo::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x67e18)
    #8 0x7fe383a08494 in testing::TestCase::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x68494)
    #9 0x7fe383a0ce05 in testing::internal::UnitTestImpl::RunAllTests() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x6ce05)
    #10 0x7fe383a0d3f7 in testing::UnitTest::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x6d3f7)
    #11 0x55eec3a8aedc in main (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x26edc)
    #12 0x7fe3803bcb96 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21b96)
    #13 0x55eec3a8b1a9 in _start (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x271a9)
0x61300001b090 is located 16 bytes inside of 352-byte region [0x61300001b080,0x61300001b1e0)
allocated by thread T0 here:
    #0 0x7fe383d4cb40 in __interceptor_malloc (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xdeb40)
    #1 0x7fe38352b5ec in Eigen::internal::aligned_malloc(unsigned long) (/root/ros_ws/install/lib/libmoveit_robot_model.so.1.0.1+0x1145ec)
SUMMARY: AddressSanitizer: bad-free (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xde7a8) in __interceptor_free
==8292==ABORTING
=================================================================
==8386==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x6120000094d0 in thread T0
    #0 0x7efe0a9b67a8 in __interceptor_free (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xde7a8)
    #1 0x7efdf31aefc9 in KDL::ChainIkSolverPos_LMA::~ChainIkSolverPos_LMA() (/opt/ros/melodic/lib/liborocos-kdl.so.1.4+0x39fc9)
    #2 0x7efdf362fcc3 in lma_kinematics_plugin::LMAKinematicsPlugin::searchPositionIK(geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, double, std::vector<double, std::allocator<double> > const&, std::vector<double, std::allocator<double> >&, boost::function<void (geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&)> const&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&, kinematics::KinematicsQueryOptions const&) const (/root/ros_ws/devel/.private/moveit_kinematics/lib//libmoveit_lma_kinematics_plugin.so+0x1ccc3)
    #3 0x7efdf361f2ec in lma_kinematics_plugin::LMAKinematicsPlugin::searchPositionIK(geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, double, std::vector<double, std::allocator<double> > const&, std::vector<double, std::allocator<double> >&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&, kinematics::KinematicsQueryOptions const&) const (/root/ros_ws/devel/.private/moveit_kinematics/lib//libmoveit_lma_kinematics_plugin.so+0xc2ec)
    #4 0x558184728ac1 in KinematicsTest_randomWalkIK_Test::TestBody() (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x3aac1)
    #5 0x7efe0a6aa31e in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0xa031e)
    #6 0x7efe0a6719b5 in testing::Test::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x679b5)
    #7 0x7efe0a671e18 in testing::TestInfo::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x67e18)
    #8 0x7efe0a672494 in testing::TestCase::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x68494)
    #9 0x7efe0a676e05 in testing::internal::UnitTestImpl::RunAllTests() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x6ce05)
    #10 0x7efe0a6773f7 in testing::UnitTest::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x6d3f7)
    #11 0x558184714edc in main (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x26edc)
    #12 0x7efe07026b96 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21b96)
    #13 0x5581847151a9 in _start (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x271a9)
0x6120000094d0 is located 16 bytes inside of 304-byte region [0x6120000094c0,0x6120000095f0)
allocated by thread T0 here:
    #0 0x7efe0a9b6b40 in __interceptor_malloc (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xdeb40)
    #1 0x7efe0a1955ec in Eigen::internal::aligned_malloc(unsigned long) (/root/ros_ws/install/lib/libmoveit_robot_model.so.1.0.1+0x1145ec)
SUMMARY: AddressSanitizer: bad-free (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xde7a8) in __interceptor_free
==8386==ABORTING
=================================================================
==8429==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x612000008150 in thread T0
    #0 0x7f39fdecb7a8 in __interceptor_free (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xde7a8)
    #1 0x7f39e66aefc9 in KDL::ChainIkSolverPos_LMA::~ChainIkSolverPos_LMA() (/opt/ros/melodic/lib/liborocos-kdl.so.1.4+0x39fc9)
    #2 0x7f39e6b2fcc3 in lma_kinematics_plugin::LMAKinematicsPlugin::searchPositionIK(geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, double, std::vector<double, std::allocator<double> > const&, std::vector<double, std::allocator<double> >&, boost::function<void (geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&)> const&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&, kinematics::KinematicsQueryOptions const&) const (/root/ros_ws/devel/.private/moveit_kinematics/lib//libmoveit_lma_kinematics_plugin.so+0x1ccc3)
    #3 0x7f39e6b1f2ec in lma_kinematics_plugin::LMAKinematicsPlugin::searchPositionIK(geometry_msgs::Pose_<std::allocator<void> > const&, std::vector<double, std::allocator<double> > const&, double, std::vector<double, std::allocator<double> > const&, std::vector<double, std::allocator<double> >&, moveit_msgs::MoveItErrorCodes_<std::allocator<void> >&, kinematics::KinematicsQueryOptions const&) const (/root/ros_ws/devel/.private/moveit_kinematics/lib//libmoveit_lma_kinematics_plugin.so+0xc2ec)
    #4 0x563f74e23ad5 in KinematicsTest_unitIK_Test::TestBody() (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x42ad5)
    #5 0x7f39fdbbf31e in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0xa031e)
    #6 0x7f39fdb869b5 in testing::Test::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x679b5)
    #7 0x7f39fdb86e18 in testing::TestInfo::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x67e18)
    #8 0x7f39fdb87494 in testing::TestCase::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x68494)
    #9 0x7f39fdb8be05 in testing::internal::UnitTestImpl::RunAllTests() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x6ce05)
    #10 0x7f39fdb8c3f7 in testing::UnitTest::Run() (/root/ros_ws/build/moveit_kinematics/gtest/googlemock/gtest/libgtest.so+0x6d3f7)
    #11 0x563f74e07edc in main (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x26edc)
    #12 0x7f39fa53bb96 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21b96)
    #13 0x563f74e081a9 in _start (/root/ros_ws/devel/.private/moveit_kinematics/lib/moveit_kinematics/test_kinematics_plugin+0x271a9)
0x612000008150 is located 16 bytes inside of 304-byte region [0x612000008140,0x612000008270)
allocated by thread T0 here:
    #0 0x7f39fdecbb40 in __interceptor_malloc (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xdeb40)
    #1 0x7f39fd6aa5ec in Eigen::internal::aligned_malloc(unsigned long) (/root/ros_ws/install/lib/libmoveit_robot_model.so.1.0.1+0x1145ec)
SUMMARY: AddressSanitizer: bad-free (/usr/lib/x86_64-linux-gnu/libasan.so.4+0xde7a8) in __interceptor_free
==8429==ABORTING
```
