#include "opencv2/opencv.hpp"
#include <iostream>
 
using namespace std;
using namespace cv;
 
void read_video(string video_path);

int main()
{
  read_video("smile.mov");
}

void read_video(string video_path)
{
	VideoCapture cap(video_path); 
	if(!cap.isOpened())
	{
		cout << "Could't read the video: " << video_path << endl;
		return;
	}

	Mat frame;
	cap >> frame;

	while (!frame.empty())
	{
		imshow("Video", frame);
		if(waitKey(25) == 27)
			break;

		cap >> frame;
	}
	
	cap.release();
	destroyAllWindows();
}