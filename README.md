# Driven_SWE_DDF
This Repository includes a new application of DDF to the field of Fluid Physics, specifically the Shallow Water Equations. In an Effort to make DDF a useful tool in the field of weather forecasting we have adapted DDF to handle the Shallow Water Equations (SWE). We tackle the interesting problem of handling a reduced dimensional data set, meaning we are trying to study a data set that doesn't observe all obesrvable quantities in a physical system. Since it is impossible to measure the infinite number of data points across all of the ocean, we must restrict ourselves to a limited number of observations; to recapture the lost information in this process, we use time delay embedding to learn the lost statistical information in the data (We have found that the inclusion of time delay embedding has a dramatic effect on the forecasting performance as long as a proper time delay is chosen!). DDF could have exciting uses in the area of regional weather forecasting. We exemplify this effect by generating a 10 by 10 grid of SWE data and then training and forecasting a reduced dimensional 3 by 3 grid with DDF.

The DDF Folder is the standard DDF which contains the standard Gaussian+Polynomial(1st order) python script and a jupyternotebook guide on how to use it. It also contains an example of using it on a 10 by 10 grid. Here is a video showcasing DDF's forecasting ability (the black grid) against the Shallow Water (the colorful surface):

https://user-images.githubusercontent.com/54558570/167758057-8e895c59-4acc-478c-b14e-5dceaa2da3c9.mp4

The Time Delay Embedding DDF Folder contains the TDE DDF python script as well as the jupyter notebook that guides users through it. Test data is included and an example folder is also included which contains a graph, video, and two text files of the results of a successful test. Here is a video of the regional weather forecasting ability of DDF using time delay embedding on a 3 by 3 corner of the 10 by 10 grid (The black outline is the prediction, the colorful tiles are the true SWE data):

https://user-images.githubusercontent.com/54558570/167758126-abe694a0-993e-4081-a2e9-87776b9184e9.mp4

The Shallow Water Equations:

<img width="1011" alt="Screen Shot 2022-04-25 at 11 48 09 PM" src="https://user-images.githubusercontent.com/54558570/165239371-c75c0201-be28-452c-bb57-0a2383cdbee7.png">


We include forcing terms that that are additive to the equations of motion. In the examples, a wind forcing term takes the place as our forcing term (the bold F); the form of the wind force is a an additional A*cos(2*pi*y/L) where A is a chosen coefficient, and L is the full length of the Shallow Water in the X direction). Also note that f(r) = f_0 + Beta * y

To obtain our data we used a method outlined in the following paper to generate the Shallow Waters:

Sadourny, Robert. "The dynamics of finite-difference models of the shallow-water equations." Journal of Atmospheric Sciences 32.4 (1975): 680-689.
