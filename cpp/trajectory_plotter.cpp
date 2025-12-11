/**
 * @file trajectory_plotter.cpp
 * @brief Implementation of trajectory plotting utilities
 */

#include "trajectory_plotter.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <algorithm>

namespace trajectory {

TrajectoryPlotter::TrajectoryPlotter(const PlotConfig& config)
    : config_(config) {
}

TrajectoryPlotter::~TrajectoryPlotter() = default;

bool TrajectoryPlotter::isGnuplotAvailable() {
    // Check if gnuplot is available
    int result = std::system("gnuplot --version > /dev/null 2>&1");
    return (result == 0);
}

std::string TrajectoryPlotter::writeTrajectoryData(const Trajectory& traj, int index) {
    std::string filename = "/tmp/trajectory_" + std::to_string(index) + ".dat";
    
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Failed to create data file: " << filename << std::endl;
        return "";
    }
    
    // Write header
    file << "# X Y Z\n";
    
    // Write trajectory points
    for (const auto& wp : traj) {
        file << wp.x << " " << wp.y << " " << wp.z << "\n";
    }
    
    file.close();
    return filename;
}

bool TrajectoryPlotter::saveToCSV(const std::vector<Trajectory>& trajectories,
                                  const std::string& base_filename) {
    for (size_t i = 0; i < trajectories.size(); ++i) {
        std::string filename = base_filename + "_" + std::to_string(i + 1) + ".csv";
        
        std::ofstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Failed to create CSV file: " << filename << std::endl;
            return false;
        }
        
        // Write header
        file << "Waypoint,X,Y,Z\n";
        
        // Write trajectory points
        for (size_t j = 0; j < trajectories[i].size(); ++j) {
            const auto& wp = trajectories[i][j];
            file << j << "," << wp.x << "," << wp.y << "," << wp.z << "\n";
        }
        
        file.close();
        std::cout << "✓ Saved trajectory " << (i + 1) << " to " << filename << std::endl;
    }
    
    return true;
}

bool TrajectoryPlotter::generateGnuplotScript(const std::vector<std::string>& data_files,
                                              const std::vector<std::string>& labels,
                                              const Waypoint& start,
                                              const Waypoint& end,
                                              bool is_3d) {
    std::string script_file = "/tmp/plot_script.gnu";
    
    std::ofstream script(script_file);
    if (!script.is_open()) {
        std::cerr << "Failed to create gnuplot script" << std::endl;
        return false;
    }
    
    // Set terminal and output
    script << "set terminal pngcairo size " << config_.width << "," << config_.height 
           << " enhanced font 'Arial,12'\n";
    script << "set output '" << config_.output_file << "'\n\n";
    
    // Set title and labels
    script << "set title '" << config_.title << "' font 'Arial,16'\n";
    
    if (is_3d) {
        script << "set xlabel 'X (m)' font 'Arial,12'\n";
        script << "set ylabel 'Y (m)' font 'Arial,12'\n";
        script << "set zlabel 'Z (m)' font 'Arial,12'\n";
        script << "set grid\n";
        script << "set key outside right top\n";
        script << "set view 60,30\n\n";
        
        script << "splot ";
    } else {
        script << "set xlabel 'X (m)' font 'Arial,12'\n";
        script << "set ylabel 'Y (m)' font 'Arial,12'\n";
        script << "set grid\n";
        script << "set key outside right top\n\n";
        
        script << "plot ";
    }
    
    // Plot trajectories
    for (size_t i = 0; i < data_files.size(); ++i) {
        if (i > 0) script << ", \\\n     ";
        
        std::string label = (i < labels.size() && !labels[i].empty()) ? 
                           labels[i] : ("Trajectory " + std::to_string(i + 1));
        
        if (is_3d) {
            script << "'" << data_files[i] << "' using 1:2:3 with lines lw 2 title '" 
                   << label << "'";
        } else {
            script << "'" << data_files[i] << "' using 1:2 with lines lw 2 title '" 
                   << label << "'";
        }
    }
    
    // Add start and end points
    if (config_.show_start_end) {
        if (is_3d) {
            script << ", \\\n     '-' using 1:2:3 with points pt 7 ps 2 lc rgb 'green' title 'Start'";
            script << ", \\\n     '-' using 1:2:3 with points pt 7 ps 2 lc rgb 'red' title 'End'";
        } else {
            script << ", \\\n     '-' using 1:2 with points pt 7 ps 2 lc rgb 'green' title 'Start'";
            script << ", \\\n     '-' using 1:2 with points pt 7 ps 2 lc rgb 'red' title 'End'";
        }
    }
    
    script << "\n";
    
    // Add start/end point data
    if (config_.show_start_end) {
        if (is_3d) {
            script << start.x << " " << start.y << " " << start.z << "\n";
            script << "e\n";
            script << end.x << " " << end.y << " " << end.z << "\n";
            script << "e\n";
        } else {
            script << start.x << " " << start.y << "\n";
            script << "e\n";
            script << end.x << " " << end.y << "\n";
            script << "e\n";
        }
    }
    
    script.close();
    
    // Execute gnuplot
    std::string command = "gnuplot " + script_file + " 2>&1";
    int result = std::system(command.c_str());
    
    if (result != 0) {
        std::cerr << "Failed to execute gnuplot" << std::endl;
        return false;
    }
    
    return true;
}

bool TrajectoryPlotter::plot3D(const std::vector<Trajectory>& trajectories,
                               const Waypoint& start,
                               const Waypoint& end,
                               const std::vector<std::string>& labels) {
    if (trajectories.empty()) {
        std::cerr << "No trajectories to plot" << std::endl;
        return false;
    }
    
    if (!isGnuplotAvailable()) {
        std::cerr << "gnuplot is not available. Please install gnuplot to use plotting features." << std::endl;
        return false;
    }
    
    std::cout << "\nGenerating 3D plot..." << std::endl;
    
    // Write trajectory data to temporary files
    std::vector<std::string> data_files;
    for (size_t i = 0; i < trajectories.size(); ++i) {
        std::string file = writeTrajectoryData(trajectories[i], i);
        if (file.empty()) {
            return false;
        }
        data_files.push_back(file);
    }
    
    // Generate and execute gnuplot script
    bool success = generateGnuplotScript(data_files, labels, start, end, true);
    
    if (success) {
        std::cout << "✓ 3D plot saved to: " << config_.output_file << std::endl;
    }
    
    // Clean up temporary files
    for (const auto& file : data_files) {
        std::remove(file.c_str());
    }
    std::remove("/tmp/plot_script.gnu");
    
    return success;
}

bool TrajectoryPlotter::plot2D(const std::vector<Trajectory>& trajectories,
                               const Waypoint& start,
                               const Waypoint& end,
                               const std::vector<std::string>& labels) {
    if (trajectories.empty()) {
        std::cerr << "No trajectories to plot" << std::endl;
        return false;
    }
    
    if (!isGnuplotAvailable()) {
        std::cerr << "gnuplot is not available. Please install gnuplot to use plotting features." << std::endl;
        return false;
    }
    
    std::cout << "\nGenerating 2D plot..." << std::endl;
    
    // Write trajectory data to temporary files
    std::vector<std::string> data_files;
    for (size_t i = 0; i < trajectories.size(); ++i) {
        std::string file = writeTrajectoryData(trajectories[i], i);
        if (file.empty()) {
            return false;
        }
        data_files.push_back(file);
    }
    
    // Generate and execute gnuplot script
    bool success = generateGnuplotScript(data_files, labels, start, end, false);
    
    if (success) {
        std::cout << "✓ 2D plot saved to: " << config_.output_file << std::endl;
    }
    
    // Clean up temporary files
    for (const auto& file : data_files) {
        std::remove(file.c_str());
    }
    std::remove("/tmp/plot_script.gnu");
    
    return success;
}

} // namespace trajectory
