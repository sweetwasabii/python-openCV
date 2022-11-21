#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;

void read_image(string image_path);

int main()
{
    read_image("cat.jpg");
}

void read_image(string image_path)
{
    Mat image = imread(image_path, IMREAD_COLOR);
    
    if(image.empty())
    {
        cout << "Could't read the image: " << image_path << endl;
        return;
    }

    imshow("Display window", image);
    if(waitKey(0) == 27)
    {
        return;
    }
}