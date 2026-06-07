#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"




class Smartphone: public rclcpp::Node
{
  public:
  Smartphone():Node("smartphone")
  {
    subscriber_=this->create_subscription<example_interfaces::msg::String>("smartphone_news",10,
      std::bind(&Smartphone::callbacknews,this,std::placeholders::_1));
      RCLCPP_INFO(this->get_logger(), "Smartphone node has been started.");

  }
private:
void callbacknews(const example_interfaces::msg::String::SharedPtr msg){
    RCLCPP_INFO(this->get_logger(),"news: %s",msg->data.c_str());

}
rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node=std::make_shared<Smartphone>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
