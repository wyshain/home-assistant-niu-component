# NIU Home Assistant integration — 国内适配版

本分支基于 marcelwestrahome 上游 **2.1.10 / a060de0**，版本 **2.1.11** 为本 fork 的国内适配版本号。固定连接中国大陆小牛账号服务器，保留上游的共享轮询、token 刷新、限流退避、双电池和轨迹相机功能。

## 2.1.11 国内适配变更

- 登录：`account.niu.com`；数据：`app-api.niu.com`。
- 请求使用 `clientIdentifier=Domestic`，与 HA 界面语言无关；语言和时区仍跟随 HA 设置。
- 总里程统计接口使用国内分支的 JSON 请求格式。
- 经纬度按国内分支的 GCJ-02 → WGS-84 近似逆变换处理。经纬度实体和连接传感器的位置属性使用同一转换入口，不修改原始缓存、不重复转换；缺失、零坐标或非法坐标返回未知值。
- `Isconnected` 从车辆数据读取 `isConnected`，与 `ScooterConnected` 一样表示车辆连接状态；布尔状态使用普通传感器，避免错误使用 binary_sensor 的 connectivity 类型。
- 保留服务端轨迹 URL，图片请求优先尝试国内路径和域名，保留查询参数。
- 保留自动 token 刷新和 HTTP 401 恢复，并对 HTTP 403 进行同样的单次恢复。尚未确认的国内业务错误码仍报错，不猜测为过期而反复登录。
- 新增简体中文，覆盖配置表单、错误提示、传感器选项、设备和实体名称。既有实体 ID 保持不变。
- 最近行程的开始、结束时间按 Home Assistant 配置的时区显示。例如设置为 `Asia/Taipei` 时显示 UTC+8。行程时长仍按持续时间显示。

坐标公式参考 [hasscc 国内分支](https://github.com/hasscc/home-assistant-niu-component)，其适用范围沿用该分支的大陆经纬度边界判断；它不是精确的国界判断。此转换只适用于接口返回 GCJ-02 的车辆。

## 安装国内版

### 全新安装

1. 将本仓库 `custom_components/niu` 完整复制到 HA 的 `/config/custom_components/niu`，然后重启 HA。
2. 在「设置 → 设备与服务 → 添加集成」搜索 **小牛电动车**（英文界面搜索 **NIU**）。
3. 输入小牛 App 账号和密码，选择车辆序号和传感器。第一辆车的序号为 `0`。选择「最近行程地图」会创建轨迹相机。

如使用 HACS，可将 `https://github.com/wyshain/home-assistant-niu-component` 添加为 Integration 自定义仓库。国内适配位于 `feat/domestic-niu`。该分支的代码可按上面的步骤手动安装。如需通过 HACS 下载国内版，须先将该提交作为默认分支或 GitHub Release 提供给 HACS。

### 已安装其他 NIU 版本

这几个版本都使用 `niu` 域，不能同时安装。替换前先备份 HA 配置与现有 `custom_components/niu`。

本 fork 保留上游配置结构；**尚不支持直接迁移 hasscc 2.0 的配置和实体身份**。国内旧版使用平铺配置及不同的 unique_id、部分属性名，上游使用 `conf_auth` 嵌套配置。请勿只覆盖文件就假定旧配置能继续工作。需要保留历史与自动化时，应先确认旧集成、配置和实体，再做迁移；全新配置则需要重新添加集成并调整引用。

## 验证与限制

单元测试（模拟 HA 与网络，不需要真实账号）：

```sh
python3.13 -m unittest discover -s tests/unit -p 'test_*.py' -v
```

47 项单元测试通过，覆盖国内请求格式、认证恢复、坐标转换、轨迹图片地址和行程时区。

已在 Home Assistant 2026.10.4 的 Docker 环境中安装，使用国内账号成功读取车辆数据。已确认设备页和配置标签显示简体中文，并核对中文化前后 28 个实体的 ID 一致。已在容器中用 HA 实际配置验证行程时区转换。真实服务器的 token 过期响应、车辆在线与离线切换及轨迹图片下载仍待验证。

## 上游说明

This custom component integrates compatible NIU vehicles with Home Assistant.

Now this integration is _asynchronous_ and it is easy installable via config flow.

## Changes:
* It automatically creates a NIU device so its sensors and camera are grouped together.
![auto device](images/niu_integration_device.png)
* If you select the Last track sensor automatically it will create a camera integration, with the rendered image of your last track.
![last track camera](images/niu_integration_camera.png)

With the thanks to pikka97 !!!

## Setup
1. In Home Assistant's settings under "device and services" click on the "Add integration" button.
2. Search for "NIU" and click on it.
3. Enter your NIU account credentials and select the sensors you want to add.
![config flow](images/config_flow_niu_integration.png)
4. Enjoy your new NIU integration :-)
