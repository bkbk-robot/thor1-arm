/**
 * ESP32-S3 + PCA9685 6-DOF 机械臂控制
 * 
 * 接线:
 * ESP32-S3          PCA9685
 * GPIO21 (SDA)  ->  SDA
 * GPIO22 (SCL)  ->  SCL
 * 5V             ->  VCC
 * GND            ->  GND
 * 
 * 舵机通道映射:
 * Ch0: 底座旋转 (Base)
 * Ch1: 大臂 (Shoulder) 
 * Ch2: 小臂 (Elbow)
 * Ch3: 手腕俯仰 (Wrist Pitch)
 * Ch4: 手腕旋转 (Wrist Roll)
 * Ch5: 夹爪 (Gripper)
 * 
 * MG996R 舵机参数:
 * 脉冲范围: 500μs-2500μs (对应0-180度)
 * PCA9685 12位分辨率: 0-4095
 * 50Hz = 20ms周期 = 20000μs
 * 500μs = 4095*500/20000 = 102
 * 2500μs = 4095*2500/20000 = 512
 */

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// I2C引脚定义 (ESP32-S3默认)
#define SDA_PIN 21
#define SCL_PIN 22

// 创建PCA9685对象
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// 舵机脉冲范围 (12位 = 0-4095)
#define SERVOMIN  102  // 500μs = 0度
#define SERVOMAX  512  // 2500μs = 180度
#define SERVO_FREQ 50  // 50Hz = 20ms周期

// 舵机通道编号
const int CH_BASE = 0;
const int CH_SHOULDER = 1;
const int CH_ELBOW = 2;
const int CH_WRIST_PITCH = 3;
const int CH_WRIST_ROLL = 4;
const int CH_GRIPPER = 5;

// 角度转脉冲值的函数
int angleToPulse(int angle) {
  // 线性映射: 0度=102, 180度=512
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

// 初始化舵机到中间位置
void initServos() {
  pwm.setPWM(CH_BASE, 0, angleToPulse(90));
  pwm.setPWM(CH_SHOULDER, 0, angleToPulse(90));
  pwm.setPWM(CH_ELBOW, 0, angleToPulse(90));
  pwm.setPWM(CH_WRIST_PITCH, 0, angleToPulse(90));
  pwm.setPWM(CH_WRIST_ROLL, 0, angleToPulse(90));
  pwm.setPWM(CH_GRIPPER, 0, angleToPulse(0)); // 夹爪关闭
}

// 移动单个舵机
// channel: 舵机通道, angle: 目标角度(0-180), delayMs: 延时毫秒
void moveServo(int channel, int angle, int delayMs = 500) {
  angle = constrain(angle, 0, 180);
  pwm.setPWM(channel, 0, angleToPulse(angle));
  delay(delayMs);
}

// 机械臂复位到初始姿势
void homePosition() {
  Serial.println("机械臂复位...");
  moveServo(CH_BASE, 90, 300);
  moveServo(CH_SHOULDER, 90, 300);
  moveServo(CH_ELBOW, 90, 300);
  moveServo(CH_WRIST_PITCH, 90, 300);
  moveServo(CH_WRIST_ROLL, 90, 300);
  moveServo(CH_GRIPPER, 0, 300); // 夹爪关闭
  Serial.println("复位完成");
}

// 测试所有舵机
void testServos() {
  Serial.println("测试舵机...");
  
  for (int ch = 0; ch < 6; ch++) {
    Serial.print("测试通道 ");
    Serial.println(ch);
    
    moveServo(ch, 0, 500);
    moveServo(ch, 180, 500);
    moveServo(ch, 90, 500);
  }
  
  Serial.println("测试完成");
}

// 夹爪控制 (0=关闭, 180=完全打开)
void setGripper(int angle) {
  moveServo(CH_GRIPPER, angle);
}

// 机械臂伸展姿势
void extendArm() {
  moveServo(CH_BASE, 90);
  moveServo(CH_SHOULDER, 0);   // 大臂抬起
  moveServo(CH_ELBOW, 180);   // 小臂伸直
  moveServo(CH_WRIST_PITCH, 90);
  moveServo(CH_WRIST_ROLL, 90);
}

// 机械臂收起姿势
void retractArm() {
  moveServo(CH_BASE, 90);
  moveServo(CH_SHOULDER, 120);
  moveServo(CH_ELBOW, 30);
  moveServo(CH_WRIST_PITCH, 90);
  moveServo(CH_WRIST_ROLL, 90);
}

// 抓取演示
void grabDemo() {
  Serial.println("抓取演示...");
  
  // 1. 伸展
  extendArm();
  delay(500);
  
  // 2. 打开夹爪
  setGripper(180);
  delay(500);
  
  // 3. 闭合夹爪
  setGripper(30);
  delay(500);
  
  // 4. 收起
  retractArm();
  delay(500);
  
  Serial.println("抓取完成");
}

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32-S3 6-DOF 机械臂控制板初始化...");
  
  // 初始化I2C
  Wire.begin(SDA_PIN, SCL_PIN);
  
  // 初始化PCA9685
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
  
  Serial.println("PCA9685 初始化完成");
  
  // 机械臂复位
  homePosition();
  
  Serial.println("初始化完成，可以开始控制");
}

void loop() {
  // 测试模式: 循环执行各种动作
  Serial.println("执行测试序列...");
  
  homePosition();
  delay(1000);
  
  testServos();
  delay(1000);
  
  grabDemo();
  delay(2000);
  
  // 也可以通过串口命令控制:
  // 格式: CH<channel>:<angle>
  // 例如: CH0:90 表示设置通道0到90度
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd.startsWith("CH")) {
      int colonIndex = cmd.indexOf(':');
      if (colonIndex > 0) {
        int ch = cmd.substring(2, colonIndex).toInt();
        int angle = cmd.substring(colonIndex + 1).toInt();
        
        if (ch >= 0 && ch <= 5 && angle >= 0 && angle <= 180) {
          Serial.print("设置通道 ");
          Serial.print(ch);
          Serial.print(" 到 ");
          Serial.println(angle);
          moveServo(ch, angle);
        }
      }
    } else if (cmd == "home") {
      homePosition();
    } else if (cmd == "test") {
      testServos();
    } else if (cmd == "grab") {
      grabDemo();
    }
  }
  
  delay(100);
}
