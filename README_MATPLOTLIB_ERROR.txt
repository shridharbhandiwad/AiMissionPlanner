╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                  MATPLOTLIB DLL ERROR - QUICK FIX                        ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

YOU'RE SEEING THIS ERROR:
═════════════════════════

  ImportError: DLL load failed while importing _c_internal_utils: 
  The specified module could not be found.


WHAT THIS MEANS:
════════════════

  Your Windows system is missing required DLL files for matplotlib.
  This is a very common issue and has a simple fix!


🚀 EASIEST FIX (FOR WINDOWS):
══════════════════════════════

  METHOD 1: Interactive Help Menu (Recommended)
  
    1. Double-click this file:
       
       CLICK_HERE_FOR_MATPLOTLIB_HELP.bat
       
    2. Choose option 1 (automatic fix)
    
    3. Wait 2-3 minutes
    
    4. Done!


  METHOD 2: Command Line Fix
  
    1. Open Command Prompt
    
    2. Navigate to project:
       cd "D:\Zoppler Projects\AiMissionPlanner"
    
    3. Activate virtual environment:
       venv\Scripts\activate
    
    4. Run fix script:
       fix_matplotlib_dll_error.bat
    
    5. Test:
       python src/data_generator.py


⏱️ TIME REQUIRED: 2-3 minutes


📚 DOCUMENTATION:
═════════════════

  Quick Reference:     FIX_MATPLOTLIB_NOW.txt
  Complete Guide:      MATPLOTLIB_DLL_FIX.md
  Summary:            MATPLOTLIB_FIX_SUMMARY.md


🔧 IF FIX DOESN'T WORK:
════════════════════════

  90% of the time, you need Visual C++ Redistributables.
  
  1. Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
  
  2. Install the downloaded file
  
  3. RESTART YOUR COMPUTER (important!)
  
  4. Run: fix_matplotlib_dll_error.bat again


❓ WHY THIS HAPPENS:
════════════════════

  • Matplotlib needs Microsoft Visual C++ runtime DLLs
  • These are NOT included with Python
  • They must be installed separately on Windows
  • Very common issue - not your fault!


✅ VERIFICATION:
════════════════

  After fix, test with:
  
  python -c "import matplotlib.pyplot as plt; print('Success!')"


🎯 ALTERNATIVE: USE CONDA
═══════════════════════════

  If pip keeps having issues, Conda works better on Windows:
  
  1. Download Miniconda: https://docs.conda.io/en/latest/miniconda.html
  2. Install Miniconda
  3. Run: conda install matplotlib numpy scipy
  4. Test: python src/data_generator.py


📞 NEED MORE HELP?
═══════════════════

  See: MATPLOTLIB_DLL_FIX.md (complete troubleshooting guide)


═══════════════════════════════════════════════════════════════════════════

                        QUICK ACTION ITEMS

═══════════════════════════════════════════════════════════════════════════

  ☐ Double-click: CLICK_HERE_FOR_MATPLOTLIB_HELP.bat
  
  ☐ Choose option 1
  
  ☐ Wait for completion
  
  ☐ Test: python src/data_generator.py

═══════════════════════════════════════════════════════════════════════════

  If that doesn't work:
  
  ☐ Install: https://aka.ms/vs/17/release/vc_redist.x64.exe
  
  ☐ Restart computer
  
  ☐ Run fix again

═══════════════════════════════════════════════════════════════════════════

                     THIS WILL BE FIXED IN 5 MINUTES!

═══════════════════════════════════════════════════════════════════════════
