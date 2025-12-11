╔════════════════════════════════════════════════════════════╗
║         EXECUTABLES NOT FOUND? READ THIS!                  ║
╚════════════════════════════════════════════════════════════╝

PROBLEM:
--------
You're trying to build on Windows but this build folder contains 
Linux executables (trajectory_app and trajectory_demo without .exe)

QUICK FIX:
----------
1. Go back to the cpp folder:
   cd ..

2. Delete this entire build folder:
   
   Command Prompt:
   rmdir /s /q build
   
   PowerShell:
   Remove-Item -Recurse -Force build
   
   Git Bash:
   rm -rf build

3. Run the build script again:
   
   PowerShell (RECOMMENDED):
   .\build.ps1
   
   Command Prompt:
   build.bat

WHY THIS HAPPENS:
-----------------
This project is developed in a Linux environment but you're building
on Windows. The build artifacts are platform-specific, so you must
clean the build folder when switching between operating systems.

AFTER CLEANING AND REBUILDING:
-------------------------------
You should see these files created:
✓ trajectory_app.exe
✓ trajectory_demo.exe
✓ libtrajectory_inference.a (or .lib)
✓ libtrajectory_metrics.a (or .lib)
✓ libtrajectory_plotter.a (or .lib)

IMPROVED BUILD SCRIPTS:
-----------------------
The build scripts have been updated to:
✓ Detect this issue and warn you
✓ Show clear progress (Step 1, 2, 3)
✓ Verify that .exe files are created
✓ List all executables at the end

MORE HELP:
----------
See: FIX_EXECUTABLE_NOT_FOUND.md in the cpp folder
