"""生成基础篇（第1-4章）知识节点、关系和来源追溯文件。

本脚本只管理 id 以 ch1_/ch2_/ch3_/ch4_ 开头的节点，以及 id 以
edge_fd_ 开头的关系；仓库中其他成员的数据会原样保留。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "backend" / "data"
NODES_FILE = DATA_DIR / "nodes.json"
EDGES_FILE = DATA_DIR / "edges.json"
TRACE_FILE = DATA_DIR / "foundation_traceability.json"

CH1 = "计算机网络概述"
CH2 = "物理层"
CH3 = "数据链路层"
CH4 = "局域网原理"
FOUNDATION_PREFIXES = ("ch1_", "ch2_", "ch3_", "ch4_")


def node(
    node_id: str,
    name: str,
    node_type: str,
    chapter: str,
    description: str,
    keywords: list[str],
    difficulty: int,
    note_refs: list[str],
    ppt_refs: list[str],
) -> dict[str, Any]:
    return {
        "id": node_id,
        "name": name,
        "type": node_type,
        "layer": "概念层",
        "chapter": chapter,
        "description": description,
        "keywords": keywords,
        "difficulty": difficulty,
        "image_urls": [],
        "video_url": None,
        "_trace": {"notes": note_refs, "slides": ppt_refs},
    }


NODES: list[dict[str, Any]] = []

# 第1章：计算机网络概述（20个）
NODES += [
    node("ch1_protocol", "网络协议", "概念", CH1,
         "协议规定网络实体交换消息的格式、顺序，以及发送、接收消息或发生事件时采取的动作。它就是网络通信双方共同遵守的“对话规则”。",
         ["协议", "消息格式", "消息顺序", "网络实体"], 1,
         ["一、导论.md#协议"], ["Chapter_1_v8.2.pptx:7-8"]),
    node("ch1_internet_overview", "Internet概览", "概念", CH1,
         "Internet既是由主机、链路、路由器和互联ISP组成的网络之网，也是向分布式应用提供通信服务和编程接口的基础设施。",
         ["Internet", "网络之网", "通信基础设施", "分布式应用"], 1,
         ["一、导论.md#网络三层结构"], ["Chapter_1_v8.2.pptx:4-6"]),
    node("ch1_network_edge", "网络边缘", "概念", CH1,
         "网络边缘由端系统构成，包括用户主机、客户端和服务器；服务器通常集中部署在数据中心。",
         ["端系统", "主机", "客户端", "服务器"], 1,
         ["一、导论.md#网络三层结构"], ["Chapter_1_v8.2.pptx:10-12"]),
    node("ch1_access_network", "接入网络", "概念", CH1,
         "接入网络把端系统连接到边缘路由器，可以是家庭有线接入、企业以太网、WiFi或蜂窝网络。共享式接入和专用式接入具有不同的带宽分配方式。",
         ["接入网络", "边缘路由器", "有线接入", "无线接入"], 2,
         ["一、导论.md#接入网络和物理介质"], ["Chapter_1_v8.2.pptx:13-20"]),
    node("ch1_physical_media", "物理介质", "概念", CH1,
         "物理介质承载bit传播。导向介质让信号沿铜线、同轴电缆或光纤传播；非导向介质让信号在开放空间以无线电波传播。",
         ["物理介质", "导向介质", "非导向介质", "bit"], 1,
         ["一、导论.md#物理介质"], ["Chapter_1_v8.2.pptx:22-24"]),
    node("ch1_network_core", "网络核心", "概念", CH1,
         "网络核心是互联路由器形成的网状结构，负责让分组沿端到端路径逐跳通过。核心功能可以概括为路由与转发。",
         ["网络核心", "路由器", "网状结构", "逐跳传输"], 1,
         ["一、导论.md#网络核心"], ["Chapter_1_v8.2.pptx:26-29"]),
    node("ch1_forwarding", "转发", "原理", CH1,
         "转发是路由器的局部动作：根据转发表，把到达输入链路的分组移动到合适的输出链路。",
         ["forwarding", "转发表", "输入链路", "输出链路"], 2,
         ["一、导论.md#网络核心两个关键功能"], ["Chapter_1_v8.2.pptx:27,29"]),
    node("ch1_routing", "路由", "原理", CH1,
         "路由是全局路径选择过程，通过路由算法决定分组从源到目的地应经过的路径；一句话就是“算路”。",
         ["routing", "路径选择", "路由算法", "源到目的"], 2,
         ["一、导论.md#网络核心两个关键功能"], ["Chapter_1_v8.2.pptx:27-28"]),
    node("ch1_packet_switching", "分组交换", "原理", CH1,
         "分组交换把应用消息切成较小的packet，让不同用户按需共享链路资源。它适合突发数据，但拥塞时会产生排队、时延和丢包。",
         ["分组交换", "packet", "资源共享", "突发数据"], 2,
         ["一、导论.md#分组交换"], ["Chapter_1_v8.2.pptx:26,30-32"]),
    node("ch1_store_and_forward", "存储转发", "原理", CH1,
         "存储转发要求路由器收到完整分组后才能向下一条链路发送。长度为L bit的分组在速率为R的链路上的发送时间为L/R。",
         ["存储转发", "分组传输时延", "L/R", "路由器"], 2,
         ["一、导论.md#分组交换"], ["Chapter_1_v8.2.pptx:30"]),
    node("ch1_queueing_packet_loss", "排队与分组丢失", "原理", CH1,
         "当分组到达输出链路的速率暂时超过链路发送能力时，分组进入缓冲区排队；缓冲区满后，新到分组会被丢弃。",
         ["排队", "缓冲区", "分组丢失", "拥塞"], 2,
         ["一、导论.md#分组交换"], ["Chapter_1_v8.2.pptx:31-32,47,55"]),
    node("ch1_circuit_switching", "电路交换", "原理", CH1,
         "电路交换在通信前建立端到端专用路径并预留资源，通信期间独占相应频带或时隙，结束后再释放。",
         ["电路交换", "资源预留", "专用路径", "FDM", "TDM"], 2,
         ["一、导论.md#电路交换"], ["Chapter_1_v8.2.pptx:33-34"]),
    node("ch1_internet_isp_structure", "Internet的ISP层次结构", "概念", CH1,
         "端系统先连接接入ISP，接入ISP再通过区域ISP、一级ISP、IXP和内容提供商网络互联，最终形成可扩展的“网络之网”。",
         ["ISP", "IXP", "一级ISP", "内容提供商网络"], 2,
         ["一、导论.md#Internet 结构"], ["Chapter_1_v8.2.pptx:37-45"]),
    node("ch1_nodal_delay", "结点总时延", "原理", CH1,
         "结点总时延由处理时延、排队时延、传输时延和传播时延组成：d_nodal=d_proc+d_queue+d_trans+d_prop。",
         ["结点时延", "处理时延", "排队时延", "传输时延", "传播时延"], 3,
         ["一、导论.md#分组延时的四种来源"], ["Chapter_1_v8.2.pptx:48-51"]),
    node("ch1_traffic_intensity", "流量强度", "原理", CH1,
         "流量强度La/R衡量输出队列负载。它接近1时平均排队时延迅速增大，大于1时到达工作量长期超过服务能力。",
         ["流量强度", "La/R", "排队时延", "链路负载"], 3,
         ["一、导论.md#排队延时"], ["Chapter_1_v8.2.pptx:52"]),
    node("ch1_throughput_bottleneck", "吞吐量与瓶颈链路", "原理", CH1,
         "吞吐量是数据成功从发送方到达接收方的速率。端到端吞吐量受路径上最慢的瓶颈链路限制，多条连接共享瓶颈时每条连接的份额会下降。",
         ["吞吐量", "瞬时吞吐量", "平均吞吐量", "瓶颈链路"], 2,
         ["一、导论.md#吞吐量"], ["Chapter_1_v8.2.pptx:56-58"]),
    node("ch1_network_security", "网络安全威胁与防御", "概念", CH1,
         "常见威胁包括分组嗅探、IP欺骗和拒绝服务攻击；防御手段包括认证、加密、完整性检查、访问限制和防火墙。",
         ["分组嗅探", "IP欺骗", "DoS", "认证", "加密", "防火墙"], 2,
         ["一、导论.md#网络安全"], ["Chapter_1_v8.2.pptx:60-65"]),
    node("ch1_internet_protocol_stack", "Internet五层协议栈", "概念", CH1,
         "Internet协议栈分为应用层、运输层、网络层、链路层和物理层。每层实现自己的服务，同时使用下一层提供的服务。",
         ["协议栈", "应用层", "运输层", "网络层", "链路层", "物理层"], 2,
         ["一、导论.md#协议层和参考模型"], ["Chapter_1_v8.2.pptx:67-71"]),
    node("ch1_encapsulation", "封装与解封装", "原理", CH1,
         "发送端把上层数据作为下层payload并逐层添加header，形成message、segment、datagram和frame；接收端按相反顺序解封装。",
         ["封装", "解封装", "header", "payload", "frame"], 2,
         ["一、导论.md#封装"], ["Chapter_1_v8.2.pptx:72-77,89"]),
    node("ch1_osi_reference_model", "OSI七层参考模型", "概念", CH1,
         "OSI模型在Internet五层协议栈基础上增加表示层和会话层。表示层处理数据表示、加密和压缩，会话层处理同步、检查点和恢复。",
         ["OSI", "表示层", "会话层", "七层模型"], 2,
         ["一、导论.md#ISO/OSI模型"], ["Chapter_1_v8.2.pptx:88"]),
]


# 第2章：物理层（第一组）
NODES += [
    node("ch2_physical_layer", "物理层", "概念", CH2,
         "物理层负责在传输介质上发送原始bit，并尽量屏蔽不同介质和通信手段的差异。它规定接口如何把比特流转换为可传输的信号。",
         ["物理层", "bit", "传输介质", "接口"], 1,
         ["二、物理层.md#基本概念"], ["Physical_Layer20260320.pptx:3"]),
    node("ch2_interface_characteristics", "物理层接口特性", "概念", CH2,
         "物理层接口由机械、电气、功能和过程四类特性共同规定，分别说明连接器形态、电压范围、信号意义和事件顺序。",
         ["机械特性", "电气特性", "功能特性", "过程特性"], 2,
         ["二、物理层.md#主要任务"], ["Physical_Layer20260320.pptx:4"]),
    node("ch2_data_signal_system", "数据通信系统与信号", "概念", CH2,
         "数据通信系统由源系统、传输系统和目的系统组成。数据是要传递的消息实体，信号是数据的电气或电磁表示，可分为模拟信号和数字信号。",
         ["数据", "信号", "模拟信号", "数字信号", "信源", "信宿"], 1,
         ["二、物理层.md#数据通信基本知识"], ["Physical_Layer20260320.pptx:5,7"]),
    node("ch2_communication_modes", "单工、半双工与全双工", "概念", CH2,
         "单工只能单向传输；半双工允许双方轮流发送但不能同时发送；全双工允许双方同时发送和接收。",
         ["单工", "半双工", "全双工", "通信方向"], 1,
         ["二、物理层.md#数据通信基本知识"], ["Physical_Layer20260320.pptx:8"]),
    node("ch2_baseband_signal_modulation", "基带信号与基带调制", "概念", CH2,
         "基带信号直接来自信源，常含低频甚至直流分量。基带调制通过改变数字信号波形来适应信道，也称为编码，处理后仍是基带信号。",
         ["基带信号", "基带调制", "编码", "低频分量"], 2,
         ["二、物理层.md#调制"], ["Physical_Layer20260320.pptx:8-9"]),
    node("ch2_line_coding", "数字线路编码", "技术", CH2,
         "常见线路编码包括不归零、归零、曼彻斯特和差分曼彻斯特编码。曼彻斯特类编码利用比特中间跳变提供自同步，但需要更高的信号频率。",
         ["不归零", "归零", "曼彻斯特编码", "差分曼彻斯特", "自同步"], 3,
         [], ["Physical_Layer20260320.pptx:10"]),
    node("ch2_bandpass_modulation", "带通调制", "技术", CH2,
         "带通调制利用载波把基带信号搬移到较高频段并转换成模拟信号，基本方式包括调幅、调频和调相。",
         ["带通调制", "载波", "调幅", "调频", "调相"], 2,
         ["二、物理层.md#调制"], ["Physical_Layer20260320.pptx:9,11"]),
    node("ch2_qam", "正交振幅调制", "技术", CH2,
         "QAM同时利用振幅和相位表示码元。星座点越多，每个码元携带的bit越多，但点间距离变小，噪声下更容易误判。",
         ["QAM", "星座图", "振幅", "相位", "码元"], 3,
         ["二、物理层.md#调制"], ["Physical_Layer20260320.pptx:12"]),
]


# 第2章：物理层（第二组）
NODES += [
    node("ch2_channel_distortion", "信道失真与码间串扰", "原理", CH2,
         "实际信道会受到带宽限制、距离、介质质量和干扰影响。码元速率过高时，相邻码元波形会互相重叠，形成码间串扰并增加判决错误。",
         ["信道失真", "码间串扰", "码元速率", "带宽"], 3,
         ["二、物理层.md#信道的极限容量"], ["Physical_Layer20260320.pptx:13-15"]),
    node("ch2_nyquist_criterion", "奈奎斯特准则", "原理", CH2,
         "奈奎斯特准则给出理想低通信道中避免码间串扰时的最高码元传输速率。信道带宽越大，可无串扰传输的码元速率上限越高。",
         ["奈奎斯特准则", "码元速率", "理想信道", "码间串扰"], 4,
         [], ["Physical_Layer20260320.pptx:15"]),
    node("ch2_snr", "信噪比", "原理", CH2,
         "信噪比S/N表示信号平均功率与噪声平均功率之比，常用SNR=10log10(S/N)换算为dB。信噪比越高，接收端越容易正确判决信号。",
         ["SNR", "信噪比", "分贝", "噪声功率"], 3,
         ["二、物理层.md#信道的极限容量"], ["Physical_Layer20260320.pptx:16"]),
    node("ch2_shannon_capacity", "香农信道容量", "原理", CH2,
         "香农公式C=Wlog2(1+S/N)给出带宽有限且存在高斯白噪声时的极限无差错信息传输速率。带宽或信噪比增大，容量上限随之提高。",
         ["香农公式", "信道容量", "带宽", "高斯白噪声"], 4,
         ["二、物理层.md#香农公式"], ["Physical_Layer20260320.pptx:17-18"]),
    node("ch2_transmission_media", "传输媒介分类", "概念", CH2,
         "传输媒介是发送端和接收端之间的物理路径，分为沿实体介质传播的导向媒介，以及在自由空间传播的非导向媒介。",
         ["传输媒介", "导向媒介", "非导向媒介", "物理路径"], 1,
         ["二、物理层.md#物理层下的传输媒介"], ["Physical_Layer20260320.pptx:20-21"]),
    node("ch2_guided_media", "导向传输媒介", "概念", CH2,
         "导向媒介包括双绞线、同轴电缆和光纤。双绞线成本低，同轴电缆抗干扰较强，光纤容量大、损耗小且不受电磁干扰。",
         ["双绞线", "同轴电缆", "光纤", "导向媒介"], 2,
         ["二、物理层.md#物理层下的传输媒介"], ["Physical_Layer20260320.pptx:22-26"]),
    node("ch2_unguided_media", "非导向传输媒介", "概念", CH2,
         "非导向媒介以自由空间为传播路径，包括无线电、微波和卫星等。传播会受到反射、遮挡、干扰和频谱管理规则影响。",
         ["无线电", "微波", "卫星", "非导向媒介", "ISM"], 2,
         ["二、物理层.md#物理层下的传输媒介"], ["Physical_Layer20260320.pptx:27-28"]),
    node("ch2_multiplexing", "信道复用", "原理", CH2,
         "信道复用让多个用户共享同一条高容量信道，通过频率、时间或码片维度区分用户，从而降低成本并提高资源利用率。",
         ["信道复用", "共享信道", "FDM", "TDM", "CDM"], 2,
         ["二、物理层.md#信道复用技术"], ["Physical_Layer20260320.pptx:30"]),
]


# 第2章：物理层（第三组）
NODES += [
    node("ch2_fdm", "频分复用", "技术", CH2,
         "FDM把信道总频带划分成多个互不重叠的子频带，每个用户在通信期间持续占用自己的频带。空闲用户对应的频带通常也不能被其他用户使用。",
         ["FDM", "频分复用", "子频带", "频谱"], 2,
         ["二、物理层.md#FDM 频分复用"], ["Physical_Layer20260320.pptx:31"]),
    node("ch2_tdm", "时分复用", "技术", CH2,
         "TDM把时间划分为周期性帧和时隙，每个用户在每帧中占用固定时隙。计算机数据具有突发性，固定分配时隙可能造成线路资源浪费。",
         ["TDM", "时分复用", "时隙", "TDM帧"], 2,
         ["二、物理层.md#TDM 时分复用"], ["Physical_Layer20260320.pptx:32-33"]),
    node("ch2_cdm", "码分复用", "技术", CH2,
         "CDM让用户在相同时间和频率上同时发送，但为每个站分配正交码片序列。接收端将叠加信号与目标站码片做规格化内积来恢复该站比特。",
         ["CDM", "CDMA", "码片序列", "正交", "规格化内积"], 4,
         ["二、物理层.md#CDM 码分复用"], ["Physical_Layer20260320.pptx:34-36"]),
    node("ch2_broadband_access", "宽带接入技术", "概念", CH2,
         "终端必须通过接入网连接ISP。宽带接入按介质可分为有线和无线方案，有线方案包括ADSL、HFC和FTTx等。",
         ["宽带接入", "ISP", "有线接入", "无线接入"], 1,
         ["二、物理层.md#宽带接入技术"], ["Physical_Layer20260320.pptx:38"]),
    node("ch2_adsl", "ADSL非对称数字用户线路", "技术", CH2,
         "ADSL利用现有电话线的高频部分传输数据，低频部分保留给传统电话。下行频带和速率通常高于上行，实际速率受距离、线径和干扰影响。",
         ["ADSL", "电话线", "非对称", "上行", "下行"], 3,
         ["二、物理层.md#ADSL 非对称数字用户线路"], ["Physical_Layer20260320.pptx:39-45"]),
    node("ch2_dmt", "DMT离散多音调制", "技术", CH2,
         "DMT是ADSL使用的多载波调制方式，本质上用FDM把高频频谱切成许多子信道，并根据各子信道质量自适应分配传输能力。",
         ["DMT", "多载波", "子信道", "自适应调制", "ADSL"], 4,
         ["二、物理层.md#DMT"], ["Physical_Layer20260320.pptx:42-44"]),
    node("ch2_hfc_cable_modem", "HFC与Cable Modem", "技术", CH2,
         "HFC在有线电视网基础上以光纤作为骨干、同轴电缆完成用户侧分配，并支持双向数据业务。用户通过Cable Modem接入共享的电缆网络。",
         ["HFC", "Cable Modem", "光纤同轴", "CATV", "共享接入"], 3,
         ["二、物理层.md#HFC 混合光纤同轴网络"], ["Physical_Layer20260320.pptx:47-50"]),
    node("ch2_fttx", "FTTx光纤接入", "技术", CH2,
         "FTTx表示光纤铺设到不同位置的接入方案。FTTH把光纤延伸到家庭，FTTB把光纤铺到楼宇后再用铜缆向用户分配。",
         ["FTTx", "FTTH", "FTTB", "光纤接入"], 2,
         ["二、物理层.md#FFx"], ["Physical_Layer20260320.pptx:51"]),
]


# 第3章：数据链路层（第一组）
NODES += [
    node("ch3_link_layer", "数据链路层", "概念", CH3,
         "链路层负责相邻节点之间的一跳数据传输。端到端路径上的不同链路可以使用不同协议，每条链路提供的可靠性和访问方式也可能不同。",
         ["链路层", "相邻节点", "一跳传输", "链路协议"], 1,
         ["四、链路层和局域网.md#简介"], ["Link_Layer20260320 (2).pptx:4-6"]),
    node("ch3_frame", "链路层帧", "概念", CH3,
         "帧是链路层的协议数据单元。发送端把网络层datagram封装在帧中并添加首部、尾部，接收端检查后再取出datagram。",
         ["frame", "帧", "datagram", "首部", "尾部"], 2,
         ["四、链路层和局域网.md#链路层实现"], ["Link_Layer20260320 (2).pptx:4,7,10"]),
    node("ch3_link_services", "链路层服务", "概念", CH3,
         "链路层可能提供成帧、链路访问、MAC寻址、可靠交付、流量控制、差错检测与纠正以及半双工/全双工等服务，但具体协议不一定全部实现。",
         ["成帧", "链路访问", "可靠交付", "流量控制", "差错检测"], 2,
         ["四、链路层和局域网.md#链路层服务"], ["Link_Layer20260320 (2).pptx:7-8"]),
    node("ch3_nic", "网络接口卡", "技术", CH3,
         "网卡NIC通常以硬件、固件和驱动组合实现链路层与物理层功能，负责发送端封装、差错位生成，以及接收端检查和解封装。",
         ["NIC", "网卡", "固件", "链路层实现"], 2,
         ["四、链路层和局域网.md#链路层实现"], ["Link_Layer20260320 (2).pptx:9-10"]),
    node("ch3_error_detection", "差错检测与纠正", "原理", CH3,
         "发送端在数据D后附加冗余的EDC，接收端按相同规则检测错误。更长的EDC通常有更强检测能力，但会增加传输开销，且检测并非百分之百可靠。",
         ["EDC", "差错检测", "差错纠正", "冗余"], 2,
         ["四、链路层和局域网.md#错误检测"], ["Link_Layer20260320 (2).pptx:12"]),
    node("ch3_parity", "奇偶校验", "原理", CH3,
         "一维奇偶校验通过增加校验位检测单bit错误；二维奇偶校验对行列分别校验，可以定位并纠正单bit错误。",
         ["奇偶校验", "一维奇偶校验", "二维奇偶校验", "单比特错误"], 2,
         ["四、链路层和局域网.md#奇偶校验"], ["Link_Layer20260320 (2).pptx:13"]),
    node("ch3_crc", "循环冗余校验", "算法", CH3,
         "CRC把数据D左移r位后用生成多项式G做模二除法，余数R作为校验位。接收端用G除收到的比特串，余数非零表示检测到错误。",
         ["CRC", "生成多项式", "模二除法", "异或", "余数"], 4,
         ["四、链路层和局域网.md#CRC：循环冗余检测"], ["Link_Layer20260320 (2).pptx:14-15"]),
    node("ch3_multiple_access_link", "多路访问链路", "概念", CH3,
         "链路分为点对点链路和广播链路。广播链路上多个节点共享介质，同时发送会产生干扰或冲突，因此需要多路访问协议协调。",
         ["点对点链路", "广播链路", "共享介质", "冲突"], 2,
         ["四、链路层和局域网.md#多路访问协议"], ["Link_Layer20260320 (2).pptx:17-18"]),
    node("ch3_ideal_mac", "理想多路访问协议", "概念", CH3,
         "理想MAC协议应让单个活跃节点获得速率R，M个活跃节点平均各得R/M，同时做到分布式、无需全局时钟并保持简单低开销。",
         ["理想MAC", "R/M", "分布式", "公平性"], 2,
         ["四、链路层和局域网.md#理想多路访问协议"], ["Link_Layer20260320 (2).pptx:19"]),
]


# 第3章：数据链路层（第二组）
NODES += [
    node("ch3_mac_taxonomy", "MAC协议分类", "概念", CH3,
         "MAC协议分为信道划分、随机访问和轮流访问三类：分别通过预分配资源、竞争后恢复以及轮流授权来共享广播信道。",
         ["MAC协议", "信道划分", "随机访问", "轮流访问"], 2,
         ["四、链路层和局域网.md#MAC 协议"], ["Link_Layer20260320 (2).pptx:20,36"]),
    node("ch3_channel_partitioning_mac", "信道划分MAC", "技术", CH3,
         "信道划分MAC把时间、频率或码空间预先分配给节点。TDMA分配固定时隙，FDMA分配固定频带，高负载时公平但低负载时可能浪费资源。",
         ["信道划分MAC", "TDMA", "FDMA", "资源预分配"], 2,
         ["四、链路层和局域网.md#信道划分 MAC"], ["Link_Layer20260320 (2).pptx:21-22"]),
    node("ch3_slotted_aloha", "时隙ALOHA", "协议", CH3,
         "时隙ALOHA要求节点只在时隙开始发送；冲突后每个节点以概率p重传。大量节点持续发送时，最大信道利用率约为1/e，即37%。",
         ["时隙ALOHA", "随机重传", "概率p", "37%"], 3,
         ["四、链路层和局域网.md#随机访问 MAC"], ["Link_Layer20260320 (2).pptx:24-26"]),
    node("ch3_pure_aloha", "纯ALOHA", "协议", CH3,
         "纯ALOHA不划分时隙，节点有帧就立即发送，任何落在两倍帧发送时间窗口内的其他发送都可能冲突，最大效率约18%。",
         ["纯ALOHA", "无时隙", "冲突窗口", "18%"], 3,
         ["四、链路层和局域网.md#随机访问 MAC"], ["Link_Layer20260320 (2).pptx:27,93"]),
    node("ch3_csma", "CSMA载波侦听多路访问", "协议", CH3,
         "CSMA在发送前先侦听信道，空闲才发送、忙则推迟。但传播时延会让两个节点都误以为信道空闲，所以仍可能碰撞。",
         ["CSMA", "载波侦听", "传播时延", "碰撞"], 3,
         ["四、链路层和局域网.md#随机访问 MAC"], ["Link_Layer20260320 (2).pptx:28-29"]),
    node("ch3_csma_cd", "CSMA/CD", "协议", CH3,
         "CSMA/CD在载波侦听基础上边发边检测碰撞，检测到碰撞就中止并发送强化信号。为检测最坏碰撞，帧发送时间必须不小于往返传播时延。",
         ["CSMA/CD", "碰撞检测", "最小帧长", "往返传播时延"], 4,
         ["四、链路层和局域网.md#随机访问 MAC"], ["Link_Layer20260320 (2).pptx:28-32"]),
    node("ch3_binary_exponential_backoff", "二进制指数退避", "算法", CH3,
         "发生第m次碰撞后，节点从0到2^m-1中随机选K，等待K×512 bit times后重试。碰撞越多，随机等待范围越大。",
         ["二进制指数退避", "随机退避", "512 bit times", "碰撞"], 4,
         ["四、链路层和局域网.md#随机访问 MAC"], ["Link_Layer20260320 (2).pptx:31"]),
    node("ch3_polling", "轮询协议", "协议", CH3,
         "轮询由中心控制器依次邀请节点发送，不会发生竞争碰撞，但存在轮询开销、等待时延和中心控制器单点故障。",
         ["Polling", "轮询", "中心控制器", "单点故障"], 2,
         ["四、链路层和局域网.md#轮流协议 MAC"], ["Link_Layer20260320 (2).pptx:33-34"]),
    node("ch3_token_passing", "令牌传递", "协议", CH3,
         "令牌传递让节点只有拿到token时才能发送，发送后再把令牌交给下一节点。它避免碰撞，但有令牌开销、等待时延和令牌丢失问题。",
         ["Token Passing", "令牌", "轮流发送", "令牌丢失"], 2,
         ["四、链路层和局域网.md#轮流协议 MAC"], ["Link_Layer20260320 (2).pptx:33,35"]),
]


# 第4章：局域网原理（第一组）
NODES += [
    node("ch4_lan", "局域网", "概念", CH4,
         "局域网在有限地理范围内连接主机和网络设备，链路层通过MAC地址、以太网帧和交换机完成同一LAN内的数据交付。",
         ["LAN", "局域网", "MAC地址", "以太网", "交换机"], 1,
         ["四、链路层和局域网.md#局域网：LAN"], ["Link_Layer20260320 (2).pptx:37-40"]),
    node("ch4_mac_address", "MAC地址", "概念", CH4,
         "MAC地址是链路层接口地址，通常为48 bit，用于在同一子网内把帧送到物理连接的接口。它与网卡接口绑定，通常不随网络位置变化。",
         ["MAC地址", "48 bit", "链路层地址", "接口"], 2,
         ["四、链路层和局域网.md#MAC 地址"], ["Link_Layer20260320 (2).pptx:38-40"]),
    node("ch4_arp", "ARP地址解析协议", "协议", CH4,
         "ARP用于在同一子网内根据IP地址查询MAC地址。请求以广播帧发送，目标主机用单播回复自己的MAC地址。",
         ["ARP", "IP地址", "MAC地址", "广播请求", "单播回复"], 3,
         ["四、链路层和局域网.md#ARP：地址解析协议"], ["Link_Layer20260320 (2).pptx:41-44"]),
    node("ch4_arp_table", "ARP表", "概念", CH4,
         "ARP表缓存IP地址、MAC地址和TTL的映射。条目到期后被遗忘，避免网络变化后长期使用过时映射。",
         ["ARP表", "地址映射", "TTL", "缓存"], 2,
         ["四、链路层和局域网.md#ARP：地址解析协议"], ["Link_Layer20260320 (2).pptx:41"]),
    node("ch4_cross_subnet_delivery", "跨子网帧交付", "原理", CH4,
         "跨子网发送时，IP源和目的地址端到端保持不变，但每经过一段链路，路由器都会去掉旧帧并用下一跳接口的MAC地址重新封装。",
         ["跨子网", "下一跳", "IP地址", "MAC地址", "重新封装"], 4,
         ["四、链路层和局域网.md#跨子网传输"], ["Link_Layer20260320 (2).pptx:45-50"]),
    node("ch4_ethernet", "以太网", "技术", CH4,
         "以太网是主流有线局域网技术，具有实现简单、成本低和速率演进快等特点。现代以太网通常采用中心交换机连接各主机。",
         ["Ethernet", "以太网", "有线局域网", "IEEE 802.3"], 1,
         ["四、链路层和局域网.md#Ethernet：以太网"], ["Link_Layer20260320 (2).pptx:52"]),
    node("ch4_ethernet_topology", "以太网物理拓扑", "概念", CH4,
         "早期以太网常用共享总线，所有节点处在同一碰撞域；现代以太网采用交换式星形结构，每条主机到交换机的链路形成独立碰撞域。",
         ["总线拓扑", "交换式以太网", "星形拓扑", "碰撞域"], 2,
         ["四、链路层和局域网.md#Ethernet：以太网"], ["Link_Layer20260320 (2).pptx:53"]),
    node("ch4_ethernet_frame", "以太网帧格式", "概念", CH4,
         "以太网帧包含前导码、目的MAC、源MAC、类型、数据和CRC。前导码用于时钟同步，类型字段标识上层协议，CRC用于差错检测。",
         ["以太网帧", "前导码", "MAC地址", "类型字段", "CRC"], 3,
         ["四、链路层和局域网.md#Ethernet 帧格式"], ["Link_Layer20260320 (2).pptx:54-55"]),
]


# 第4章：局域网原理（第二组）
NODES += [
    node("ch4_ethernet_service_model", "以太网服务模型", "原理", CH4,
         "以太网无连接且不可靠，网卡之间不握手，也不发送ACK或NAK。丢失帧只有在上层协议提供可靠传输时才可能恢复。",
         ["无连接", "不可靠", "ACK", "NAK", "CSMA/CD"], 2,
         ["四、链路层和局域网.md#Ethernet：以太网"], ["Link_Layer20260320 (2).pptx:56"]),
    node("ch4_ethernet_standards", "IEEE 802.3以太网标准", "概念", CH4,
         "不同802.3以太网标准可以使用不同速率和物理介质，但共享相同的MAC思想与基本帧格式。",
         ["IEEE 802.3", "以太网标准", "MAC协议", "物理介质"], 2,
         ["四、链路层和局域网.md#Ethernet：以太网"], ["Link_Layer20260320 (2).pptx:57"]),
    node("ch4_ethernet_switch", "以太网交换机", "技术", CH4,
         "交换机是透明、即插即用的链路层设备，存储并转发以太网帧，根据目的MAC地址选择一个或多个输出接口。",
         ["交换机", "链路层设备", "存储转发", "透明", "即插即用"], 2,
         ["四、链路层和局域网.md#交换机"], ["Link_Layer20260320 (2).pptx:59"]),
    node("ch4_collision_domain", "碰撞域与全双工交换", "概念", CH4,
         "交换式以太网中每条端口链路都是独立碰撞域，主机可与交换机全双工通信，不同端口对可以并行传输；竞争同一输出端口的帧仍需排队。",
         ["碰撞域", "全双工", "并行传输", "输出端口"], 3,
         ["四、链路层和局域网.md#交换机"], ["Link_Layer20260320 (2).pptx:60-61"]),
    node("ch4_switch_table", "交换机转发表", "概念", CH4,
         "交换机转发表保存主机MAC地址、到达该主机的接口以及时间戳，用于决定帧的定向转发、过滤或泛洪。",
         ["交换机转发表", "MAC地址", "接口号", "时间戳"], 2,
         ["四、链路层和局域网.md#交换机转发表"], ["Link_Layer20260320 (2).pptx:62"]),
    node("ch4_switch_self_learning", "交换机自学习", "算法", CH4,
         "交换机收到帧时，根据源MAC地址和进入接口学习发送主机的位置，并更新转发表；不需要额外的路由协议或人工配置。",
         ["自学习", "源MAC", "进入接口", "转发表更新"], 3,
         ["四、链路层和局域网.md#交换机转发表"], ["Link_Layer20260320 (2).pptx:63"]),
    node("ch4_switch_filter_forward", "交换机过滤、转发与泛洪", "算法", CH4,
         "目的MAC已知且不在来向接口时定向转发；与来向接口同侧时过滤丢弃；目的MAC未知时除来向接口外向其他接口泛洪。",
         ["过滤", "定向转发", "泛洪", "未知目的MAC"], 3,
         ["四、链路层和局域网.md#帧过滤 / 转发"], ["Link_Layer20260320 (2).pptx:64-65"]),
    node("ch4_switch_interconnection", "多交换机互联", "原理", CH4,
         "多个自学习交换机可以级联，学习机制会沿交换网络自动建立到远端主机的转发表项，不需要主机感知中间交换机。",
         ["交换机互联", "级联", "自学习", "远端主机"], 3,
         ["四、链路层和局域网.md#交换机"], ["Link_Layer20260320 (2).pptx:66-67"]),
]


# 第4章：局域网原理（第三组）
NODES += [
    node("ch4_switch_vs_router", "交换机与路由器对比", "概念", CH4,
         "两者都采用存储转发并维护转发表，但交换机检查链路层首部、按MAC地址自学习；路由器检查网络层首部、按IP地址和路由算法计算路径。",
         ["交换机", "路由器", "MAC地址", "IP地址", "转发表"], 3,
         ["四、链路层和局域网.md#交换机"], ["Link_Layer20260320 (2).pptx:68"]),
    node("ch4_vlan", "虚拟局域网", "技术", CH4,
         "VLAN在同一物理交换基础设施上划分多个逻辑广播域，以减少广播范围并改善管理、安全和隐私；不同VLAN间通信需要网络层路由。",
         ["VLAN", "逻辑局域网", "广播域", "流量隔离"], 3,
         ["四、链路层和局域网.md#VLAN 虚拟局域网"], ["Link_Layer20260320 (2).pptx:70-73"]),
    node("ch4_port_based_vlan", "基于端口的VLAN", "技术", CH4,
         "基于端口的VLAN由交换机管理软件把端口分组，同组端口属于同一逻辑LAN。端口也可以动态改变VLAN归属。",
         ["端口VLAN", "端口分组", "动态成员", "流量隔离"], 2,
         ["四、链路层和局域网.md#VLAN 虚拟局域网"], ["Link_Layer20260320 (2).pptx:72-73"]),
    node("ch4_vlan_trunk_8021q", "VLAN Trunk与802.1Q", "协议", CH4,
         "Trunk链路在交换机之间承载多个VLAN的帧。802.1Q为帧加入包含VLAN ID和优先级的标签，并因帧内容变化重新计算CRC。",
         ["trunk", "802.1Q", "VLAN ID", "VLAN标签", "CRC"], 4,
         ["四、链路层和局域网.md#VLAN 虚拟局域网"], ["Link_Layer20260320 (2).pptx:74-75"]),
    node("ch4_datacenter_network", "数据中心网络", "概念", CH4,
         "数据中心网络连接大量服务器、机架顶部交换机和更高层交换机，需要同时处理大规模请求、可靠性、负载均衡和网络瓶颈。",
         ["数据中心", "服务器机架", "TOR交换机", "网络瓶颈"], 3,
         ["四、链路层和局域网.md#数据中心网络"], ["Link_Layer20260320 (2).pptx:77-79"]),
    node("ch4_datacenter_multipath", "数据中心多路径", "原理", CH4,
         "数据中心交换机和机架之间通常提供多条可选路径，以并行利用带宽提高吞吐量，并在链路或设备故障时通过冗余提高可靠性。",
         ["多路径", "吞吐量", "冗余", "可靠性"], 3,
         ["四、链路层和局域网.md#多路径"], ["Link_Layer20260320 (2).pptx:80"]),
    node("ch4_load_balancer", "负载均衡器", "技术", CH4,
         "负载均衡器接收外部客户端请求，选择数据中心内的服务器或服务器组处理，并把结果返回给客户端，同时隐藏内部结构。",
         ["负载均衡器", "应用层路由", "服务器", "工作负载"], 3,
         ["四、链路层和局域网.md#负载均衡器"], ["Link_Layer20260320 (2).pptx:81"]),
    node("ch4_web_request_lifecycle", "Web请求的跨层工作流程", "原理", CH4,
         "主机接入网络后依次使用DHCP获取配置、ARP解析下一跳MAC、DNS解析域名、TCP建立连接并通过HTTP交换网页，过程中数据逐层封装和转发。",
         ["DHCP", "ARP", "DNS", "TCP", "HTTP", "跨层流程"], 5,
         [], ["Link_Layer20260320 (2).pptx:83-90"]),
]


EDGE_SPECS: list[tuple[str, str, str, str]] = [
    # 第1章
    ("ch1_internet_overview", "ch1_protocol", "包含", "Internet中的通信活动由协议约束"),
    ("ch1_internet_overview", "ch1_network_edge", "包含", "Internet结构包含网络边缘"),
    ("ch1_internet_overview", "ch1_access_network", "包含", "Internet结构包含接入网络"),
    ("ch1_internet_overview", "ch1_network_core", "包含", "Internet结构包含网络核心"),
    ("ch1_internet_overview", "ch1_internet_isp_structure", "包含", "Internet由多层ISP和内容网络互联"),
    ("ch1_access_network", "ch1_physical_media", "包含", "接入网络通过有线或无线物理介质连接端系统"),
    ("ch1_network_core", "ch1_forwarding", "包含", "网络核心中的路由器执行局部转发"),
    ("ch1_network_core", "ch1_routing", "包含", "网络核心通过路由算法选择端到端路径"),
    ("ch1_forwarding", "ch1_routing", "对比", "转发是局部按表移动，路由是全局路径计算"),
    ("ch1_network_core", "ch1_packet_switching", "包含", "Internet核心主要采用分组交换"),
    ("ch1_packet_switching", "ch1_store_and_forward", "包含", "分组交换路由器采用存储转发"),
    ("ch1_packet_switching", "ch1_queueing_packet_loss", "包含", "分组交换在拥塞时出现排队和丢包"),
    ("ch1_packet_switching", "ch1_circuit_switching", "对比", "分组交换共享资源，电路交换预留专用资源"),
    ("ch1_store_and_forward", "ch1_nodal_delay", "应用于", "存储转发产生链路传输时延"),
    ("ch1_queueing_packet_loss", "ch1_nodal_delay", "应用于", "排队是结点总时延的重要组成"),
    ("ch1_traffic_intensity", "ch1_queueing_packet_loss", "前置知识", "流量强度决定排队时延和拥塞趋势"),
    ("ch1_physical_media", "ch1_nodal_delay", "应用于", "链路距离和信号速度决定传播时延"),
    ("ch1_packet_switching", "ch1_throughput_bottleneck", "应用于", "共享链路和瓶颈限制端到端吞吐量"),
    ("ch1_internet_overview", "ch1_network_security", "包含", "Internet体系需要考虑攻击与防御"),
    ("ch1_internet_overview", "ch1_internet_protocol_stack", "包含", "Internet使用分层协议栈组织复杂功能"),
    ("ch1_protocol", "ch1_internet_protocol_stack", "前置知识", "理解协议是理解协议分层的前提"),
    ("ch1_internet_protocol_stack", "ch1_encapsulation", "包含", "分层通信通过逐层封装实现"),
    ("ch1_internet_protocol_stack", "ch1_osi_reference_model", "对比", "Internet五层栈与OSI七层模型层次不同"),
    ("ch1_network_security", "ch1_internet_protocol_stack", "应用于", "安全机制需要在协议栈各层考虑"),
]

EDGE_SPECS += [
    # 第2章
    ("ch1_physical_media", "ch2_physical_layer", "前置知识", "概述中的物理介质引出物理层的详细机制"),
    ("ch1_access_network", "ch2_broadband_access", "前置知识", "接入网络概念是学习宽带接入技术的基础"),
    ("ch2_physical_layer", "ch2_interface_characteristics", "包含", "物理层协议规定四类接口特性"),
    ("ch2_physical_layer", "ch2_data_signal_system", "包含", "物理层处理数据与信号的转换和传输"),
    ("ch2_data_signal_system", "ch2_communication_modes", "包含", "通信系统可以采用单工、半双工或全双工"),
    ("ch2_data_signal_system", "ch2_baseband_signal_modulation", "包含", "信源产生的基带信号需要适配信道"),
    ("ch2_baseband_signal_modulation", "ch2_line_coding", "包含", "线路编码是典型基带调制方式"),
    ("ch2_baseband_signal_modulation", "ch2_bandpass_modulation", "对比", "基带调制改变波形，带通调制搬移频谱"),
    ("ch2_bandpass_modulation", "ch2_qam", "包含", "QAM是同时利用振幅和相位的带通调制"),
    ("ch2_channel_distortion", "ch2_nyquist_criterion", "包含", "奈奎斯特准则描述带宽限制下的码元速率上限"),
    ("ch2_channel_distortion", "ch2_snr", "包含", "噪声强弱是影响接收判决的重要因素"),
    ("ch2_snr", "ch2_shannon_capacity", "前置知识", "香农公式使用线性信噪比S/N计算容量"),
    ("ch2_nyquist_criterion", "ch2_shannon_capacity", "对比", "奈奎斯特关注无噪声码元上限，香农关注有噪声信息容量"),
    ("ch2_physical_layer", "ch2_transmission_media", "包含", "物理层bit依赖传输媒介传播"),
    ("ch2_transmission_media", "ch2_guided_media", "包含", "传输媒介包括导向介质"),
    ("ch2_transmission_media", "ch2_unguided_media", "包含", "传输媒介包括非导向介质"),
    ("ch2_physical_layer", "ch2_multiplexing", "包含", "物理层使用复用技术共享信道"),
    ("ch2_multiplexing", "ch2_fdm", "包含", "频分复用按频带区分用户"),
    ("ch2_multiplexing", "ch2_tdm", "包含", "时分复用按周期时隙区分用户"),
    ("ch2_multiplexing", "ch2_cdm", "包含", "码分复用按正交码片区分用户"),
    ("ch2_fdm", "ch2_tdm", "对比", "FDM让用户同时占不同频带，TDM让用户轮流占同一频带"),
    ("ch2_fdm", "ch2_dmt", "前置知识", "DMT以频分方式划分大量子载波"),
    ("ch2_broadband_access", "ch2_adsl", "包含", "ADSL是利用电话线的有线宽带接入"),
    ("ch2_broadband_access", "ch2_hfc_cable_modem", "包含", "HFC是基于有线电视网的宽带接入"),
    ("ch2_broadband_access", "ch2_fttx", "包含", "FTTx是光纤宽带接入方案"),
    ("ch2_adsl", "ch2_dmt", "包含", "ADSL采用DMT多载波调制"),
    ("ch2_guided_media", "ch2_adsl", "应用于", "ADSL使用铜质电话双绞线"),
    ("ch2_guided_media", "ch2_hfc_cable_modem", "应用于", "HFC结合光纤和同轴电缆"),
    ("ch2_guided_media", "ch2_fttx", "应用于", "FTTx以光纤作为主要接入介质"),
    ("ch2_adsl", "ch2_hfc_cable_modem", "对比", "ADSL通常独享用户线，HFC用户共享电缆接入段"),
]

EDGE_SPECS += [
    # 第3章
    ("ch1_internet_protocol_stack", "ch3_link_layer", "包含", "链路层是Internet五层协议栈的一层"),
    ("ch1_encapsulation", "ch3_frame", "应用于", "网络层datagram在链路层被封装为frame"),
    ("ch2_physical_layer", "ch3_link_layer", "前置知识", "链路层使用物理层提供的bit传输服务"),
    ("ch3_link_layer", "ch3_frame", "包含", "链路层以帧为协议数据单元"),
    ("ch3_link_layer", "ch3_link_services", "包含", "链路层可提供成帧、访问、可靠性和差错处理等服务"),
    ("ch3_link_layer", "ch3_nic", "包含", "主机的链路层功能主要由NIC实现"),
    ("ch3_link_services", "ch3_error_detection", "包含", "差错检测与纠正属于链路层服务"),
    ("ch3_error_detection", "ch3_parity", "包含", "奇偶校验是一类基础差错检测方法"),
    ("ch3_error_detection", "ch3_crc", "包含", "CRC是链路中广泛使用的差错检测方法"),
    ("ch3_parity", "ch3_crc", "对比", "奇偶校验简单但能力弱，CRC可检测多类突发错误"),
    ("ch3_link_services", "ch3_multiple_access_link", "包含", "共享广播链路需要链路访问控制"),
    ("ch3_multiple_access_link", "ch3_ideal_mac", "包含", "理想MAC给出共享信道的目标性质"),
    ("ch3_multiple_access_link", "ch3_mac_taxonomy", "包含", "多路访问协议按资源分配方式分为三类"),
    ("ch3_mac_taxonomy", "ch3_channel_partitioning_mac", "包含", "信道划分是MAC协议的一类"),
    ("ch3_mac_taxonomy", "ch3_slotted_aloha", "包含", "时隙ALOHA属于随机访问MAC"),
    ("ch3_mac_taxonomy", "ch3_pure_aloha", "包含", "纯ALOHA属于随机访问MAC"),
    ("ch3_slotted_aloha", "ch3_pure_aloha", "对比", "时隙ALOHA通过同步时隙缩小冲突窗口并提高效率"),
    ("ch3_mac_taxonomy", "ch3_csma", "包含", "CSMA属于载波侦听随机访问MAC"),
    ("ch3_csma", "ch3_csma_cd", "前置知识", "CSMA/CD在CSMA基础上增加碰撞检测"),
    ("ch3_csma_cd", "ch3_binary_exponential_backoff", "包含", "碰撞后的重传等待采用二进制指数退避"),
    ("ch3_mac_taxonomy", "ch3_polling", "包含", "轮询属于轮流访问MAC"),
    ("ch3_mac_taxonomy", "ch3_token_passing", "包含", "令牌传递属于轮流访问MAC"),
    ("ch3_polling", "ch3_token_passing", "对比", "轮询依赖中心控制器，令牌传递依赖分布式token"),
    ("ch2_tdm", "ch3_channel_partitioning_mac", "应用于", "TDMA把TDM思想用于多节点信道访问"),
    ("ch2_fdm", "ch3_channel_partitioning_mac", "应用于", "FDMA把FDM思想用于多节点信道访问"),
]

EDGE_SPECS += [
    # 第4章（局域网与以太网）
    ("ch3_link_layer", "ch4_lan", "应用于", "局域网是链路层技术的主要应用场景"),
    ("ch4_lan", "ch4_mac_address", "包含", "LAN接口使用MAC地址完成本地寻址"),
    ("ch4_mac_address", "ch4_arp", "前置知识", "ARP把IP地址解析为链路层MAC地址"),
    ("ch4_arp", "ch4_arp_table", "包含", "ARP使用缓存表保存IP与MAC映射"),
    ("ch4_arp", "ch4_cross_subnet_delivery", "应用于", "跨子网发送前需要解析下一跳接口MAC地址"),
    ("ch1_encapsulation", "ch4_cross_subnet_delivery", "应用于", "每一跳都重新进行链路层封装和解封装"),
    ("ch4_lan", "ch4_ethernet", "包含", "以太网是主流有线LAN技术"),
    ("ch4_ethernet", "ch4_ethernet_topology", "包含", "以太网经历了共享总线到交换式拓扑的演进"),
    ("ch4_ethernet", "ch4_ethernet_frame", "包含", "以太网定义统一的链路层帧格式"),
    ("ch3_frame", "ch4_ethernet_frame", "应用于", "以太网帧是链路层frame的具体实现"),
    ("ch3_crc", "ch4_ethernet_frame", "应用于", "以太网帧尾部使用CRC检测差错"),
    ("ch4_ethernet", "ch4_ethernet_service_model", "包含", "以太网提供无连接、不可靠的链路层服务"),
    ("ch3_csma_cd", "ch4_ethernet_service_model", "应用于", "共享式以太网使用CSMA/CD访问介质"),
    ("ch4_ethernet", "ch4_ethernet_standards", "包含", "IEEE 802.3包含多种速率和介质标准"),
    ("ch2_transmission_media", "ch4_ethernet_standards", "应用于", "不同以太网标准采用铜缆或光纤等介质"),
    ("ch4_ethernet", "ch4_ethernet_switch", "包含", "现代以太网使用交换机转发帧"),
    ("ch4_ethernet_topology", "ch4_collision_domain", "包含", "交换式拓扑把每条端口链路分成独立碰撞域"),
    ("ch4_ethernet_switch", "ch4_collision_domain", "包含", "交换机支持独立碰撞域和全双工并行通信"),
    ("ch4_ethernet_switch", "ch4_switch_table", "包含", "交换机依据转发表选择输出接口"),
    ("ch4_switch_table", "ch4_switch_self_learning", "依赖", "转发表内容由源MAC自学习产生和更新"),
]

EDGE_SPECS += [
    # 第4章（交换、VLAN与数据中心）
    ("ch4_switch_table", "ch4_switch_filter_forward", "依赖", "过滤、定向转发和泛洪决策依赖转发表查询"),
    ("ch4_switch_self_learning", "ch4_switch_filter_forward", "前置知识", "先理解表项学习，才能理解目的地址转发决策"),
    ("ch4_ethernet_switch", "ch4_switch_interconnection", "包含", "自学习交换机可以透明互联"),
    ("ch4_switch_self_learning", "ch4_switch_interconnection", "应用于", "多交换机网络仍通过源MAC自学习建立路径"),
    ("ch1_forwarding", "ch4_switch_vs_router", "应用于", "交换机和路由器都会执行存储转发"),
    ("ch1_routing", "ch4_switch_vs_router", "应用于", "路由器使用路由算法计算IP转发表，交换机通过自学习建立MAC表"),
    ("ch4_ethernet_switch", "ch4_switch_vs_router", "对比", "交换机工作在链路层，路由器工作在网络层"),
    ("ch4_lan", "ch4_vlan", "包含", "VLAN在物理LAN之上划分逻辑广播域"),
    ("ch4_vlan", "ch4_port_based_vlan", "包含", "端口分组是VLAN的常见实现方式"),
    ("ch4_vlan", "ch4_vlan_trunk_8021q", "包含", "跨交换机VLAN使用Trunk和802.1Q标签"),
    ("ch4_ethernet_frame", "ch4_vlan_trunk_8021q", "前置知识", "802.1Q在标准以太网帧中插入标签并重算CRC"),
    ("ch4_lan", "ch4_datacenter_network", "应用于", "数据中心由大规模高速交换网络连接服务器"),
    ("ch4_datacenter_network", "ch4_datacenter_multipath", "包含", "数据中心使用多路径提升吞吐和可靠性"),
    ("ch4_datacenter_network", "ch4_load_balancer", "包含", "负载均衡器负责把外部请求分配给内部服务器"),
    ("ch1_throughput_bottleneck", "ch4_datacenter_multipath", "应用于", "多路径可分散瓶颈并提高机架间吞吐量"),
    ("ch4_arp", "ch4_web_request_lifecycle", "应用于", "Web请求发送前通过ARP获得首跳MAC地址"),
    ("ch4_ethernet", "ch4_web_request_lifecycle", "应用于", "DHCP、DNS、TCP和HTTP报文在LAN内封装进以太网帧"),
    ("ch4_ethernet_switch", "ch4_web_request_lifecycle", "应用于", "交换机在主机和首跳路由器之间转发帧"),
    ("ch1_encapsulation", "ch4_web_request_lifecycle", "应用于", "Web访问展示应用到物理层的逐层封装与解封装"),
]


def read_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json_atomic(path: Path, payload: Any) -> None:
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temp_path.replace(path)


def main() -> None:
    existing_nodes = read_json(NODES_FILE)
    existing_edges = read_json(EDGES_FILE)

    trace_by_node = {item["id"]: item.pop("_trace") for item in NODES}
    generated_ids = {item["id"] for item in NODES}
    if len(generated_ids) != len(NODES):
        raise ValueError("基础篇节点存在重复 id")

    preserved_nodes = [
        item for item in existing_nodes
        if not item.get("id", "").startswith(FOUNDATION_PREFIXES)
    ]
    preserved_ids = {item["id"] for item in preserved_nodes}
    collisions = generated_ids & preserved_ids
    if collisions:
        raise ValueError(f"节点 id 与其他成员数据冲突: {sorted(collisions)}")

    generated_edges = [
        {
            "id": f"edge_fd_{index:03d}",
            "source": source,
            "target": target,
            "relation": relation,
            "description": description,
        }
        for index, (source, target, relation, description) in enumerate(EDGE_SPECS, start=1)
    ]
    preserved_edges = [
        item for item in existing_edges
        if not item.get("id", "").startswith("edge_fd_")
    ]

    merged_nodes = preserved_nodes + NODES
    merged_edges = preserved_edges + generated_edges
    all_node_ids = {item["id"] for item in merged_nodes}
    edge_ids = [item["id"] for item in merged_edges]
    if len(edge_ids) != len(set(edge_ids)):
        raise ValueError("关系 id 重复")
    dangling = [
        item["id"] for item in merged_edges
        if item["source"] not in all_node_ids or item["target"] not in all_node_ids
    ]
    if dangling:
        raise ValueError(f"存在悬空关系: {dangling}")

    allowed_types = {"概念", "协议", "算法", "原理", "技术"}
    allowed_chapters = {CH1, CH2, CH3, CH4}
    for item in NODES:
        if item["type"] not in allowed_types:
            raise ValueError(f"不支持的节点类型: {item['id']} -> {item['type']}")
        if item["chapter"] not in allowed_chapters:
            raise ValueError(f"不支持的章节: {item['id']} -> {item['chapter']}")
        if not 1 <= item["difficulty"] <= 5:
            raise ValueError(f"难度越界: {item['id']}")

    edge_trace = {}
    for item in generated_edges:
        sources = []
        for endpoint in (item["source"], item["target"]):
            endpoint_trace = trace_by_node.get(endpoint, {})
            for kind in ("notes", "slides"):
                for ref in endpoint_trace.get(kind, []):
                    entry = {"kind": kind, "ref": ref}
                    if entry not in sources:
                        sources.append(entry)
        edge_trace[item["id"]] = {
            "source": item["source"],
            "target": item["target"],
            "relation": item["relation"],
            "rationale": item["description"],
            "evidence": sources,
        }

    trace_payload = {
        "scope": "基础篇：计算机网络概述、物理层、数据链路层、局域网原理",
        "generation": {
            "script": "scripts/generate_foundation_graph.py",
            "managed_node_prefixes": list(FOUNDATION_PREFIXES),
            "managed_edge_prefix": "edge_fd_",
            "node_count": len(NODES),
            "edge_count": len(generated_edges),
        },
        "source_catalog": {
            "一、导论.md": "<user-home>/Desktop/大二下笔记/已考完/计算机网络笔记/一、导论.md",
            "二、物理层.md": "<user-home>/Desktop/大二下笔记/已考完/计算机网络笔记/二、物理层.md",
            "四、链路层和局域网.md": "<user-home>/Desktop/大二下笔记/已考完/计算机网络笔记/四、链路层和局域网.md",
            "Chapter_1_v8.2.pptx": "<user-home>/Documents/WeChat Files/.../2026-03/Chapter_1_v8.2.pptx",
            "Physical_Layer20260320.pptx": "<user-home>/Documents/WeChat Files/.../2026-03/Physical_Layer20260320.pptx",
            "Link_Layer20260320 (2).pptx": "<user-home>/Documents/WeChat Files/.../2026-04/Link_Layer20260320 (2).pptx",
        },
        "nodes": trace_by_node,
        "edges": edge_trace,
    }

    write_json_atomic(NODES_FILE, merged_nodes)
    write_json_atomic(EDGES_FILE, merged_edges)
    write_json_atomic(TRACE_FILE, trace_payload)
    print(
        f"基础篇生成完成: {len(NODES)} 个节点, {len(generated_edges)} 条关系; "
        f"合并后共 {len(merged_nodes)} 个节点, {len(merged_edges)} 条关系"
    )


if __name__ == "__main__":
    main()
