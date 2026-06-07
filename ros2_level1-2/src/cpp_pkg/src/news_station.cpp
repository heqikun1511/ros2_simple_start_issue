#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class Newsstation : public rclcpp::Node
{

public:
    Newsstation() : Node("newsstation")
    {   this->declare_parameter("timer_period", 1);
        publisher_ = this->create_publisher<example_interfaces::msg::String>("news", 10);
        timer_ = this->create_wall_timer(std::chrono::seconds(this->get_parameter("timer_period").as_int()), std::bind(&Newsstation::pulish_news, this));
        RCLCPP_INFO(this->get_logger(), "News station has been started.");
    }
   

private:
    void pulish_news()
    {
        auto msg = example_interfaces::msg::String();
        msg.data = "hello world";
        publisher_->publish(msg);//发布消息
    }
    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_ ;
};

int main(int argc, char **argv)
{

    rclcpp::init(argc, argv);
    auto node = std::make_shared<Newsstation>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}