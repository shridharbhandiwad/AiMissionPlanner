/**
 * @file trajectory_plotter.h
 * @brief Plotting utilities for trajectories using gnuplot
 * @author Mission Planner Team
 */

#ifndef TRAJECTORY_PLOTTER_H
#define TRAJECTORY_PLOTTER_H

#include "trajectory_inference.h"
#include <string>
#include <vector>

namespace trajectory {

/**
 * @brief Configuration for plotting
 */
struct PlotConfig {
    std::string output_file = "trajectories.png";
    std::string title = "Generated Trajectories";
    int width = 1200;
    int height = 900;
    bool show_3d = true;
    bool show_start_end = true;
    bool save_data = true;
    
    PlotConfig() = default;
};

/**
 * @brief Trajectory plotter using gnuplot
 */
class TrajectoryPlotter {
public:
    /**
     * @brief Constructor
     * @param config Plot configuration
     */
    explicit TrajectoryPlotter(const PlotConfig& config = PlotConfig());
    
    /**
     * @brief Destructor
     */
    ~TrajectoryPlotter();
    
    /**
     * @brief Plot multiple trajectories in 3D
     * @param trajectories Vector of trajectories to plot
     * @param start Starting waypoint
     * @param end Ending waypoint
     * @param labels Optional labels for each trajectory
     * @return True if successful
     */
    bool plot3D(const std::vector<Trajectory>& trajectories,
                const Waypoint& start,
                const Waypoint& end,
                const std::vector<std::string>& labels = {});
    
    /**
     * @brief Plot multiple trajectories in 2D (X-Y projection)
     * @param trajectories Vector of trajectories to plot
     * @param start Starting waypoint
     * @param end Ending waypoint
     * @param labels Optional labels for each trajectory
     * @return True if successful
     */
    bool plot2D(const std::vector<Trajectory>& trajectories,
                const Waypoint& start,
                const Waypoint& end,
                const std::vector<std::string>& labels = {});
    
    /**
     * @brief Save trajectory data to CSV files
     * @param trajectories Vector of trajectories
     * @param base_filename Base filename for CSV files
     * @return True if successful
     */
    bool saveToCSV(const std::vector<Trajectory>& trajectories,
                   const std::string& base_filename = "trajectory");
    
    /**
     * @brief Check if gnuplot is available
     * @return True if gnuplot is available
     */
    static bool isGnuplotAvailable();
    
private:
    PlotConfig config_;
    
    /**
     * @brief Write trajectory to temporary file
     */
    std::string writeTrajectoryData(const Trajectory& traj, int index);
    
    /**
     * @brief Generate gnuplot script
     */
    bool generateGnuplotScript(const std::vector<std::string>& data_files,
                              const std::vector<std::string>& labels,
                              const Waypoint& start,
                              const Waypoint& end,
                              bool is_3d);
};

} // namespace trajectory

#endif // TRAJECTORY_PLOTTER_H
