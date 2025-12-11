/**
 * @file trajectory_app.cpp
 * @brief Main application for trajectory generation with plotting
 * 
 * This application:
 * 1. Takes start point, end point, and number of waypoints as input
 * 2. Generates top 5 diverse trajectories
 * 3. Ranks them by quality metrics
 * 4. Plots them in 3D
 */

#include "trajectory_inference.h"
#include "trajectory_plotter.h"
#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <sstream>
#include <cstring>
#include <chrono>

using namespace trajectory;

/**
 * @brief Trajectory ranking metrics
 */
struct TrajectoryRanking {
    int index;
    float path_length;
    float smoothness;
    float efficiency;
    float score;
    
    bool operator<(const TrajectoryRanking& other) const {
        return score > other.score;  // Higher score is better
    }
};

/**
 * @brief Compute combined quality score for trajectory
 */
float computeQualityScore(const Trajectory& traj) {
    float length = computePathLength(traj);
    float smoothness = computeSmoothnessScore(traj);
    
    // Compute straight-line distance
    float dx = traj.back().x - traj.front().x;
    float dy = traj.back().y - traj.front().y;
    float dz = traj.back().z - traj.front().z;
    float straight_dist = std::sqrt(dx*dx + dy*dy + dz*dz);
    
    float efficiency = (length > 0) ? (straight_dist / length) : 0.0f;
    
    // Combined score (weighted)
    // Prefer: high smoothness (weight=0.5), high efficiency (weight=0.3), shorter paths (weight=0.2)
    float normalized_length = std::min(1.0f, 1000.0f / std::max(100.0f, length));
    float score = 0.5f * smoothness + 0.3f * efficiency + 0.2f * normalized_length;
    
    return score;
}

/**
 * @brief Rank trajectories by quality
 */
std::vector<TrajectoryRanking> rankTrajectories(const std::vector<Trajectory>& trajectories) {
    std::vector<TrajectoryRanking> rankings;
    
    for (size_t i = 0; i < trajectories.size(); ++i) {
        TrajectoryRanking ranking;
        ranking.index = i;
        ranking.path_length = computePathLength(trajectories[i]);
        ranking.smoothness = computeSmoothnessScore(trajectories[i]);
        
        // Compute efficiency
        const auto& traj = trajectories[i];
        float dx = traj.back().x - traj.front().x;
        float dy = traj.back().y - traj.front().y;
        float dz = traj.back().z - traj.front().z;
        float straight_dist = std::sqrt(dx*dx + dy*dy + dz*dz);
        ranking.efficiency = (ranking.path_length > 0) ? (straight_dist / ranking.path_length) : 0.0f;
        
        ranking.score = computeQualityScore(trajectories[i]);
        
        rankings.push_back(ranking);
    }
    
    // Sort by score (descending)
    std::sort(rankings.begin(), rankings.end());
    
    return rankings;
}

/**
 * @brief Print usage information
 */
void printUsage(const char* program_name) {
    std::cout << "Usage: " << program_name << " [options]\n\n";
    std::cout << "Options:\n";
    std::cout << "  --start X Y Z          Starting point coordinates (default: 0 0 100)\n";
    std::cout << "  --end X Y Z            Ending point coordinates (default: 800 600 200)\n";
    std::cout << "  --waypoints N          Number of waypoints in trajectory (default: 50)\n";
    std::cout << "  --model PATH           Path to ONNX model (default: ../models/trajectory_generator.onnx)\n";
    std::cout << "  --norm PATH            Path to normalization JSON (default: ../models/trajectory_generator_normalization.json)\n";
    std::cout << "  --output FILE          Output plot filename (default: trajectories.png)\n";
    std::cout << "  --no-plot              Disable plotting (only generate trajectories)\n";
    std::cout << "  --csv                  Save trajectories to CSV files\n";
    std::cout << "  --help                 Show this help message\n\n";
    std::cout << "Examples:\n";
    std::cout << "  " << program_name << " --start 0 0 100 --end 1000 800 300\n";
    std::cout << "  " << program_name << " --start -500 300 150 --end 600 -400 250 --waypoints 75\n";
    std::cout << "  " << program_name << " --output my_trajectories.png --csv\n";
}

/**
 * @brief Parse command line arguments
 */
struct AppConfig {
    Waypoint start{0.0f, 0.0f, 100.0f};
    Waypoint end{800.0f, 600.0f, 200.0f};
    int num_waypoints = 50;
    std::string model_path = "../models/trajectory_generator.onnx";
    std::string norm_path = "../models/trajectory_generator_normalization.json";
    std::string output_file = "trajectories.png";
    bool enable_plot = true;
    bool save_csv = false;
};

bool parseArguments(int argc, char* argv[], AppConfig& config) {
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        
        if (arg == "--help" || arg == "-h") {
            printUsage(argv[0]);
            return false;
        } else if (arg == "--start") {
            if (i + 3 >= argc) {
                std::cerr << "Error: --start requires 3 arguments (X Y Z)" << std::endl;
                return false;
            }
            config.start.x = std::stof(argv[++i]);
            config.start.y = std::stof(argv[++i]);
            config.start.z = std::stof(argv[++i]);
        } else if (arg == "--end") {
            if (i + 3 >= argc) {
                std::cerr << "Error: --end requires 3 arguments (X Y Z)" << std::endl;
                return false;
            }
            config.end.x = std::stof(argv[++i]);
            config.end.y = std::stof(argv[++i]);
            config.end.z = std::stof(argv[++i]);
        } else if (arg == "--waypoints") {
            if (i + 1 >= argc) {
                std::cerr << "Error: --waypoints requires an argument" << std::endl;
                return false;
            }
            config.num_waypoints = std::stoi(argv[++i]);
            if (config.num_waypoints < 2 || config.num_waypoints > 200) {
                std::cerr << "Error: waypoints must be between 2 and 200" << std::endl;
                return false;
            }
        } else if (arg == "--model") {
            if (i + 1 >= argc) {
                std::cerr << "Error: --model requires an argument" << std::endl;
                return false;
            }
            config.model_path = argv[++i];
        } else if (arg == "--norm") {
            if (i + 1 >= argc) {
                std::cerr << "Error: --norm requires an argument" << std::endl;
                return false;
            }
            config.norm_path = argv[++i];
        } else if (arg == "--output") {
            if (i + 1 >= argc) {
                std::cerr << "Error: --output requires an argument" << std::endl;
                return false;
            }
            config.output_file = argv[++i];
        } else if (arg == "--no-plot") {
            config.enable_plot = false;
        } else if (arg == "--csv") {
            config.save_csv = true;
        } else {
            std::cerr << "Error: Unknown argument '" << arg << "'" << std::endl;
            return false;
        }
    }
    
    return true;
}

int main(int argc, char* argv[]) {
    std::cout << "========================================" << std::endl;
    std::cout << "Trajectory Generator - C++ Application" << std::endl;
    std::cout << "========================================" << std::endl;
    
    // Parse arguments
    AppConfig config;
    if (!parseArguments(argc, argv, config)) {
        return 1;
    }
    
    // Print configuration
    std::cout << "\nConfiguration:" << std::endl;
    std::cout << "  Start point: [" << config.start.x << ", " << config.start.y << ", " << config.start.z << "]" << std::endl;
    std::cout << "  End point:   [" << config.end.x << ", " << config.end.y << ", " << config.end.z << "]" << std::endl;
    std::cout << "  Waypoints:   " << config.num_waypoints << std::endl;
    std::cout << "  Model:       " << config.model_path << std::endl;
    std::cout << "  Output:      " << config.output_file << std::endl;
    
    try {
        // Initialize generator
        std::cout << "\n--- Initializing Generator ---" << std::endl;
        
        GeneratorConfig gen_config(config.model_path);
        gen_config.latent_dim = 64;
        gen_config.seq_len = config.num_waypoints;
        gen_config.num_threads = 4;
        
        TrajectoryGenerator generator(gen_config);
        
        // Load normalization
        if (!generator.loadNormalization(config.norm_path)) {
            std::cerr << "Warning: Failed to load normalization, using defaults" << std::endl;
        }
        
        // Generate diverse trajectories
        std::cout << "\n--- Generating Trajectories ---" << std::endl;
        std::cout << "Generating 10 candidate trajectories..." << std::endl;
        
        auto start_time = std::chrono::high_resolution_clock::now();
        
        int n_candidates = 10;
        std::vector<Trajectory> all_trajectories = generator.generateMultiple(
            config.start, config.end, n_candidates
        );
        
        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
        
        std::cout << "✓ Generated " << n_candidates << " trajectories in " 
                  << duration.count() << " ms" << std::endl;
        
        // Rank trajectories
        std::cout << "\n--- Ranking Trajectories ---" << std::endl;
        auto rankings = rankTrajectories(all_trajectories);
        
        std::cout << "\nTop 5 Trajectories (ranked by quality):\n" << std::endl;
        std::cout << std::setw(5) << "Rank" 
                  << std::setw(12) << "Length(m)"
                  << std::setw(12) << "Smoothness"
                  << std::setw(12) << "Efficiency"
                  << std::setw(12) << "Score" << std::endl;
        std::cout << std::string(53, '-') << std::endl;
        
        std::vector<Trajectory> top5_trajectories;
        std::vector<std::string> labels;
        
        for (int i = 0; i < std::min(5, static_cast<int>(rankings.size())); ++i) {
            const auto& rank = rankings[i];
            std::cout << std::setw(5) << (i + 1)
                      << std::setw(12) << std::fixed << std::setprecision(1) << rank.path_length
                      << std::setw(12) << std::fixed << std::setprecision(4) << rank.smoothness
                      << std::setw(12) << std::fixed << std::setprecision(3) << rank.efficiency
                      << std::setw(12) << std::fixed << std::setprecision(4) << rank.score
                      << std::endl;
            
            top5_trajectories.push_back(all_trajectories[rank.index]);
            labels.push_back("Trajectory #" + std::to_string(i + 1) + " (Score: " + 
                           std::to_string(rank.score).substr(0, 5) + ")");
        }
        
        // Save detailed stats
        std::cout << "\n--- Detailed Statistics ---" << std::endl;
        for (size_t i = 0; i < top5_trajectories.size(); ++i) {
            std::cout << "\nTrajectory " << (i + 1) << ":" << std::endl;
            printTrajectoryStats(top5_trajectories[i]);
        }
        
        // Save to CSV if requested
        if (config.save_csv) {
            std::cout << "\n--- Saving to CSV ---" << std::endl;
            PlotConfig plot_config;
            TrajectoryPlotter plotter(plot_config);
            plotter.saveToCSV(top5_trajectories, "trajectory");
        }
        
        // Plot trajectories
        if (config.enable_plot) {
            std::cout << "\n--- Generating Plot ---" << std::endl;
            
            if (!TrajectoryPlotter::isGnuplotAvailable()) {
                std::cerr << "⚠ Warning: gnuplot not available. Skipping plot generation." << std::endl;
                std::cerr << "  Install gnuplot to enable plotting: sudo apt install gnuplot (Linux)" << std::endl;
            } else {
                PlotConfig plot_config;
                plot_config.output_file = config.output_file;
                plot_config.title = "Top 5 Generated Trajectories";
                plot_config.width = 1400;
                plot_config.height = 1000;
                plot_config.show_3d = true;
                plot_config.show_start_end = true;
                
                TrajectoryPlotter plotter(plot_config);
                
                if (plotter.plot3D(top5_trajectories, config.start, config.end, labels)) {
                    std::cout << "✓ Plot saved successfully!" << std::endl;
                } else {
                    std::cerr << "✗ Failed to generate plot" << std::endl;
                }
            }
        }
        
        // Summary
        std::cout << "\n========================================" << std::endl;
        std::cout << "Summary" << std::endl;
        std::cout << "========================================" << std::endl;
        std::cout << "✓ Generated " << top5_trajectories.size() << " high-quality trajectories" << std::endl;
        std::cout << "✓ Average path length: " << std::fixed << std::setprecision(1);
        
        float avg_length = 0.0f;
        for (const auto& traj : top5_trajectories) {
            avg_length += computePathLength(traj);
        }
        avg_length /= top5_trajectories.size();
        std::cout << avg_length << " m" << std::endl;
        
        if (config.save_csv) {
            std::cout << "✓ Trajectories saved to CSV files" << std::endl;
        }
        
        if (config.enable_plot && TrajectoryPlotter::isGnuplotAvailable()) {
            std::cout << "✓ Visualization saved to: " << config.output_file << std::endl;
        }
        
        std::cout << "\n✓ Application completed successfully!" << std::endl;
        std::cout << "========================================" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "\n❌ Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
