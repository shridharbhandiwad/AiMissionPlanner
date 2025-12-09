/**
 * @file main.cpp
 * @brief Example usage of trajectory generation in C++
 */

#include "trajectory_inference.h"
#include <iostream>
#include <iomanip>
#include <chrono>

using namespace trajectory;

void printWaypoint(const Waypoint& wp, const std::string& label) {
    std::cout << label << ": [" 
              << std::fixed << std::setprecision(2)
              << wp.x << ", " << wp.y << ", " << wp.z << "]" << std::endl;
}

void printTrajectory(const Trajectory& traj, int max_points = 5) {
    std::cout << "Trajectory with " << traj.size() << " waypoints:" << std::endl;
    
    int n_show = std::min(max_points, static_cast<int>(traj.size()));
    
    for (int i = 0; i < n_show; ++i) {
        std::cout << "  [" << i << "] ";
        printWaypoint(traj[i], "");
    }
    
    if (traj.size() > max_points) {
        std::cout << "  ..." << std::endl;
        std::cout << "  [" << traj.size()-1 << "] ";
        printWaypoint(traj.back(), "");
    }
}

int main(int argc, char* argv[]) {
    std::cout << "========================================" << std::endl;
    std::cout << "Trajectory Generation - C++ Demo" << std::endl;
    std::cout << "========================================" << std::endl;
    
    // Parse command line arguments
    std::string model_path = "models/trajectory_generator.onnx";
    std::string norm_path = "models/trajectory_generator_normalization.json";
    
    if (argc > 1) {
        model_path = argv[1];
    }
    if (argc > 2) {
        norm_path = argv[2];
    }
    
    std::cout << "\nConfiguration:" << std::endl;
    std::cout << "  Model: " << model_path << std::endl;
    std::cout << "  Normalization: " << norm_path << std::endl;
    
    try {
        // Create generator
        std::cout << "\n--- Initializing Generator ---" << std::endl;
        
        GeneratorConfig config(model_path);
        config.latent_dim = 64;
        config.seq_len = 50;
        config.num_threads = 4;
        
        TrajectoryGenerator generator(config);
        
        // Load normalization
        if (!generator.loadNormalization(norm_path)) {
            std::cerr << "Warning: Failed to load normalization, using defaults" << std::endl;
        }
        
        // Example 1: Generate single trajectory
        std::cout << "\n--- Example 1: Single Trajectory ---" << std::endl;
        
        Waypoint start1(0.0f, 0.0f, 100.0f);
        Waypoint end1(800.0f, 600.0f, 200.0f);
        
        printWaypoint(start1, "Start");
        printWaypoint(end1, "End");
        
        auto t1_start = std::chrono::high_resolution_clock::now();
        Trajectory traj1 = generator.generate(start1, end1);
        auto t1_end = std::chrono::high_resolution_clock::now();
        
        auto duration1 = std::chrono::duration_cast<std::chrono::milliseconds>(t1_end - t1_start);
        
        std::cout << "\n✓ Generated trajectory in " << duration1.count() << " ms" << std::endl;
        printTrajectory(traj1, 5);
        
        std::cout << std::endl;
        printTrajectoryStats(traj1);
        
        // Example 2: Generate multiple diverse trajectories
        std::cout << "\n--- Example 2: Multiple Diverse Trajectories ---" << std::endl;
        
        Waypoint start2(-500.0f, 300.0f, 150.0f);
        Waypoint end2(600.0f, -400.0f, 250.0f);
        
        printWaypoint(start2, "Start");
        printWaypoint(end2, "End");
        
        int n_samples = 5;
        std::cout << "\nGenerating " << n_samples << " trajectories..." << std::endl;
        
        auto t2_start = std::chrono::high_resolution_clock::now();
        std::vector<Trajectory> trajectories = generator.generateMultiple(start2, end2, n_samples);
        auto t2_end = std::chrono::high_resolution_clock::now();
        
        auto duration2 = std::chrono::duration_cast<std::chrono::milliseconds>(t2_end - t2_start);
        
        std::cout << "\n✓ Generated " << n_samples << " trajectories in " 
                  << duration2.count() << " ms" << std::endl;
        std::cout << "  Avg time per trajectory: " 
                  << duration2.count() / static_cast<float>(n_samples) << " ms" << std::endl;
        
        // Compare trajectories
        std::cout << "\nComparison:" << std::endl;
        for (size_t i = 0; i < trajectories.size(); ++i) {
            float length = computePathLength(trajectories[i]);
            float smoothness = computeSmoothnessScore(trajectories[i]);
            
            std::cout << "  Trajectory " << i+1 << ": "
                      << "Length=" << std::fixed << std::setprecision(1) << length << "m, "
                      << "Smoothness=" << std::fixed << std::setprecision(4) << smoothness
                      << std::endl;
        }
        
        // Example 3: Batch processing
        std::cout << "\n--- Example 3: Batch Processing ---" << std::endl;
        
        int n_batch = 100;
        std::cout << "Generating " << n_batch << " trajectories..." << std::endl;
        
        auto t3_start = std::chrono::high_resolution_clock::now();
        
        for (int i = 0; i < n_batch; ++i) {
            // Random start and end (for demonstration)
            Waypoint start_rand(
                (i % 10 - 5) * 100.0f,
                (i % 7 - 3) * 100.0f,
                100.0f + (i % 5) * 50.0f
            );
            
            Waypoint end_rand(
                ((i + 5) % 10 - 5) * 100.0f,
                ((i + 3) % 7 - 3) * 100.0f,
                150.0f + ((i + 2) % 5) * 50.0f
            );
            
            generator.generate(start_rand, end_rand);
        }
        
        auto t3_end = std::chrono::high_resolution_clock::now();
        auto duration3 = std::chrono::duration_cast<std::chrono::milliseconds>(t3_end - t3_start);
        
        std::cout << "✓ Generated " << n_batch << " trajectories in " 
                  << duration3.count() << " ms" << std::endl;
        std::cout << "  Avg time per trajectory: " 
                  << duration3.count() / static_cast<float>(n_batch) << " ms" << std::endl;
        std::cout << "  Throughput: " 
                  << (n_batch * 1000.0f) / duration3.count() << " trajectories/sec" << std::endl;
        
        std::cout << "\n========================================" << std::endl;
        std::cout << "Demo completed successfully!" << std::endl;
        std::cout << "========================================" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "\n❌ Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
