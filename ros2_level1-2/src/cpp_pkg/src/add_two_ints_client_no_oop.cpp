#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"


int main(int args,char**argv){

    rclcpp::init(args,argv);
    auto node=rclcpp::Node::make_shared("add_two_ints_client");
    auto client=node->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints_client");
    while(client->wait_for_service(std::chrono::seconds(1))){
        RCLCPP_INFO(node->get_logger(),"service is not available, waiting again...");
    }
    auto request=std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
    request->a=1;
    request->b=2;
    auto result_future=client->async_send_request(request);
    rclcpp::spin_until_future_complete(node,result_future);
    auto result=result_future.get();
    RCLCPP_INFO(node->get_logger(),"Result: %d",result->sum);
    rclcpp::shutdown();
    return 0;






}