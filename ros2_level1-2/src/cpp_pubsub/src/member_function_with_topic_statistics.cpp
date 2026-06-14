#include <chrono>//设置时间间隔
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp/subscription_options.hpp"

#include "std_msgs/msg/string.hpp"

class MinimalSubscriberWithTopicStatistics : public rclcpp::Node
{
public:
  MinimalSubscriberWithTopicStatistics()
  : Node("minimal_subscriber_with_topic_statistics")
  {
  
    auto options = rclcpp::SubscriptionOptions();//自定义订阅行为
    options.topic_stats_options.state = rclcpp::TopicStatisticsState::Enable;//自动收集订阅统计数据

    
    options.topic_stats_options.publish_period = std::chrono::seconds(10);//发布周期为10sec

  

    auto callback = [this](std_msgs::msg::String::SharedPtr msg) {
        this->topic_callback(msg);
      };

    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "topic", 10, callback, options);//订阅主题名topic

  }
//topic_callback 是一个成员函数（有 this 指针），不能直接像普通函数那样传递给 
//create_subscription。这里用 Lambda 包裹一层，相当于做了一个适配器，把成员函数的调用包装成可传递的函数对象。
private:
  void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
  {
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
  }
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriberWithTopicStatistics>());
  rclcpp::shutdown();
  return 0;
}