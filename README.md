 <!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ucl-geospatial/app-repository-harrisonluft">
    <img src="images/UCL_CEGE.png" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Isle of Wight Flood Evacuation Map </h3>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
	<li><a href="#further-reading">Further Reading</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
This project is comprised of six tasks, find below a high-level description of each. See further below for a resource providing a more technical description.

### Task 1: User Input
* The user inputs their coordinates as a British National Grid coordinate and tests whether or not the user in within the bounding box of the island. If not, the application terminates. 

### Task 2: Highest Point Identification
* To avoid memory issues, the elevation raster is clipped to a 5km radius around the user's location. Maximum height and coordinates of the point are extracted from the elevation raster.

### Task 3: Locating Nearest Integrated Transport Node
* Using rtrees all nodes are inserted into a spatial index, the nearest transport node is identified via the nearest() method. An ITN node is identified for both the user's and the highest point location. 

### Task 4: Shortest Path 
* Using Naismith's rule a shortest route by time is calculated. For each segment a weight is calculated based on elevation and distance. Applying dijkstra's algorithm a shorest route is found.

### Task 5: Plotting the Route
* A map consisting of the start and end points and the route along the transport network is presented along with the elevation raster.

### Task 6: Extending the Region
* As noted in Task 1, the routing application is limited to user points within 5km of the edge of the island (to avoid input points starting in the sea). To overcome this, a spatial indexing and intersection technique is applied to identify points within the Isle of Wight.

## Futher Reading
* The companion report to this project can be found within the github repository under **Flood Emergency Plan - Isle of Wight.pdf**
