#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"
#include <iostream>

class Add_two_ints_server: public rclcpp::Node
{
  public:
  Add_two_ints_server():Node("add_two_ints")
  {
    service_=this->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints",
        std::bind(&Add_two_ints_server::callbacknews,this,std::placeholders::_1,std::placeholders::_2));
        RCLCPP_INFO(this->get_logger(), "Add two ints server has been started.");

  }
private:
void callbacknews(const example_interfaces::srv::AddTwoInts::Request::SharedPtr request,
 const example_interfaces::srv::AddTwoInts::Response::SharedPtr response)
{
response->sum=request->a+request->b;
    RCLCPP_INFO(this->get_logger(),"request: a=%ld, b=%ld",request->a,request->b);
}
  rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service_;
};


int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node=std::make_shared<Add_two_ints_server>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}