"""生成并合并核心篇（第5-7章）知识图谱数据。

脚本以章节为边界管理核心篇数据，保留基础篇和前沿篇成员的数据。根目录
``data/core`` 保存模块独立交付文件，``backend/data`` 保存平台运行时聚合数据。
"""

from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "data" / "core"
BACKEND_DATA = ROOT / "backend" / "data"
CORE_CHAPTERS = {"网络层", "传输层", "应用层"}
ALLOWED_NODE_TYPES = {"协议", "概念", "技术", "算法", "设备", "服务"}
LETTERS = "ABCD"


def kp(node_id: str, name: str, node_type: str, chapter: str, description: str,
       keywords: list[str], difficulty: int = 3) -> dict[str, Any]:
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
    }


NETWORK_NODES = [
    kp("core_ch5_network_layer", "网络层", "概念", "网络层", "网络层负责把分组从源主机逐跳交付到目的主机，核心任务包括逻辑寻址、路由选择和分组转发。", ["分组交付", "逻辑寻址", "路由", "转发"], 1),
    kp("core_ch5_ip_service", "IP数据报服务", "服务", "网络层", "网际协议向上层提供无连接、尽最大努力交付的数据报服务，不保证可靠性、顺序或时延。", ["无连接", "尽最大努力", "数据报", "不可靠交付"], 2),
    kp("core_ch5_ipv4", "IPv4协议", "协议", "网络层", "IPv4使用32位地址标识接口，并通过数据报首部支持分片、生存时间和上层协议标识等功能。", ["32位地址", "数据报", "TTL", "分片"], 2),
    kp("core_ch5_ipv4_header", "IPv4数据报首部", "概念", "网络层", "IPv4首部通常为20字节，包含版本、首部长度、总长度、标识、分片字段、TTL、协议和首部检验和等。", ["总长度", "TTL", "首部检验和", "分片偏移"], 3),
    kp("core_ch5_ipv4_addressing", "IPv4地址", "概念", "网络层", "IPv4地址由网络前缀和主机号组成，采用点分十进制表示，并分配给网络接口而非抽象主机本身。", ["网络前缀", "主机号", "点分十进制", "接口"], 2),
    kp("core_ch5_classful_addressing", "分类编址", "技术", "网络层", "分类编址把IPv4单播地址划分为A、B、C类网络，网络号长度固定，容易产生地址空间浪费。", ["A类", "B类", "C类", "网络号"], 2),
    kp("core_ch5_subnet_mask", "子网掩码", "概念", "网络层", "子网掩码以连续的1标识网络前缀，以连续的0标识主机部分，可与IPv4地址按位与得到网络地址。", ["按位与", "网络地址", "前缀长度", "掩码"], 2),
    kp("core_ch5_subnetting", "子网划分", "技术", "网络层", "子网划分从主机号借位形成子网号，使一个地址块可按组织结构拆分为多个更小广播域。", ["借位", "子网号", "可用主机", "广播地址"], 3),
    kp("core_ch5_cidr", "无分类域间路由CIDR", "技术", "网络层", "CIDR使用可变长度前缀a.b.c.d/x描述地址块，支持路由聚合并提高IPv4地址利用率。", ["CIDR", "可变长前缀", "地址块", "路由聚合"], 3),
    kp("core_ch5_longest_prefix", "最长前缀匹配", "算法", "网络层", "路由器在多条匹配路由中选择网络前缀最长的一条，使更具体的路由优先于聚合路由。", ["最长匹配", "转发表", "具体路由", "下一跳"], 3),
    kp("core_ch5_ipv6", "IPv6协议", "协议", "网络层", "IPv6使用128位地址和固定40字节基本首部，扩大地址空间并简化中间路由器处理。", ["128位地址", "固定首部", "扩展首部", "下一首部"], 2),
    kp("core_ch5_ipv6_header", "IPv6基本首部", "概念", "网络层", "IPv6基本首部包含版本、流量类别、流标签、有效载荷长度、下一首部和跳数限制等字段，不含首部检验和。", ["流标签", "跳数限制", "下一首部", "有效载荷长度"], 3),
    kp("core_ch5_transition", "IPv4向IPv6过渡", "技术", "网络层", "双协议栈、隧道和协议转换可使IPv4与IPv6网络在长期过渡阶段互通。", ["双协议栈", "隧道", "协议转换", "过渡机制"], 3),
    kp("core_ch5_arp", "地址解析协议ARP", "协议", "网络层", "ARP在同一链路上依据IPv4地址查询对应MAC地址，请求通常广播，响应通常单播，并将结果缓存。", ["IP到MAC", "广播请求", "单播响应", "ARP缓存"], 2),
    kp("core_ch5_icmp", "网际控制报文协议ICMP", "协议", "网络层", "ICMP封装在IP数据报中传递差错报告和询问信息，例如目的不可达、超时与回显请求。", ["差错报告", "目的不可达", "超时", "回显"], 2),
    kp("core_ch5_ping", "Ping诊断", "技术", "网络层", "Ping利用ICMP回显请求与回显回答测试目的主机可达性，并估计往返时间和丢包情况。", ["回显请求", "回显回答", "RTT", "可达性"], 2),
    kp("core_ch5_traceroute", "Traceroute路径探测", "技术", "网络层", "Traceroute逐步增加TTL或跳数限制，利用中间路由器返回的ICMP超时报文识别路径上的各跳。", ["TTL", "逐跳探测", "ICMP超时", "路径"], 3),
    kp("core_ch5_nat", "网络地址转换NAT", "技术", "网络层", "NAT在边界设备上改写私网地址与端口，使多台内部主机共享少量公网IPv4地址。", ["私网地址", "公网地址", "端口映射", "NAPT"], 3),
    kp("core_ch5_router", "路由器", "设备", "网络层", "路由器连接不同网络，依据转发表执行逐包转发，并通过路由协议学习或计算可达路径。", ["路由器", "输入端口", "交换结构", "输出端口"], 2),
    kp("core_ch5_forwarding_table", "转发表", "概念", "网络层", "转发表记录目的前缀、下一跳和输出接口，是路由器数据平面实施转发决策的直接依据。", ["目的前缀", "下一跳", "输出接口", "数据平面"], 2),
    kp("core_ch5_routing_algorithm", "路由选择算法", "算法", "网络层", "路由选择算法依据拓扑和链路代价计算源到目的的较优路径，并把结果用于生成转发表。", ["路径选择", "链路代价", "拓扑", "控制平面"], 3),
    kp("core_ch5_distance_vector", "距离向量算法", "算法", "网络层", "距离向量算法依据Bellman-Ford思想与邻居交换距离向量，分布式迭代更新到各目的网络的代价。", ["Bellman-Ford", "距离向量", "邻居交换", "计数到无穷"], 4),
    kp("core_ch5_link_state", "链路状态算法", "算法", "网络层", "链路状态算法通过泛洪获得全网拓扑，再在本地运行Dijkstra算法计算最短路径树。", ["链路状态", "泛洪", "Dijkstra", "最短路径树"], 4),
    kp("core_ch5_rip", "RIP协议", "协议", "网络层", "RIP是基于距离向量的内部网关协议，以跳数为度量，最大有效距离为15跳并周期交换路由信息。", ["距离向量", "跳数", "15跳", "内部网关协议"], 3),
    kp("core_ch5_ospf", "OSPF协议", "协议", "网络层", "OSPF是链路状态内部网关协议，使用Dijkstra算法、区域层次和链路状态通告实现快速收敛。", ["链路状态", "区域", "LSA", "Dijkstra"], 4),
    kp("core_ch5_as", "自治系统AS", "概念", "网络层", "自治系统是在统一技术管理和路由策略下运行的一组网络，对外以自治系统号标识。", ["自治系统", "ASN", "域内路由", "域间路由"], 3),
    kp("core_ch5_bgp", "BGP协议", "协议", "网络层", "BGP是自治系统之间的路径向量协议，通告AS-PATH等属性并依据策略选择可达路由。", ["路径向量", "AS-PATH", "域间路由", "路由策略"], 4),
]


TRANSPORT_NODES = [
    kp("core_ch6_transport_layer", "传输层", "概念", "传输层", "传输层在端系统中为应用进程提供端到端逻辑通信，并完成复用分用、差错检测与可选的可靠传输。", ["进程通信", "端到端", "复用分用", "可靠传输"], 1),
    kp("core_ch6_process_communication", "进程到进程通信", "服务", "传输层", "传输层把网络层的主机到主机交付扩展为应用进程之间的逻辑通信。", ["进程", "逻辑通信", "端系统", "应用数据"], 1),
    kp("core_ch6_multiplexing", "复用与分用", "技术", "传输层", "发送端把多个套接字的数据复用到传输层报文，接收端依据端口及连接标识把报文分用给正确进程。", ["复用", "分用", "套接字", "连接标识"], 2),
    kp("core_ch6_port", "端口号", "概念", "传输层", "端口号是16位进程标识，0到1023通常为熟知端口，客户端常使用临时端口。", ["16位", "熟知端口", "临时端口", "进程标识"], 2),
    kp("core_ch6_socket", "套接字端点", "概念", "传输层", "传输层套接字是应用进程使用网络服务的端点，TCP连接通常由源和目的IP地址、端口号四元组标识。", ["套接字", "四元组", "IP地址", "端口号"], 2),
    kp("core_ch6_udp", "UDP协议", "协议", "传输层", "UDP提供无连接、面向报文的尽最大努力交付，首部开销小且应用可直接控制发送时机。", ["无连接", "面向报文", "低开销", "尽最大努力"], 2),
    kp("core_ch6_udp_header", "UDP数据报首部", "概念", "传输层", "UDP首部固定8字节，依次包含源端口、目的端口、长度和检验和四个16位字段。", ["8字节", "源端口", "长度", "检验和"], 2),
    kp("core_ch6_udp_checksum", "UDP检验和", "技术", "传输层", "UDP检验和对伪首部、UDP首部和数据进行反码求和，用于检测端到端传输中的比特差错。", ["伪首部", "反码求和", "差错检测", "端到端"], 3),
    kp("core_ch6_tcp", "TCP协议", "协议", "传输层", "TCP提供面向连接、可靠、全双工的字节流服务，并实现流量控制和拥塞控制。", ["面向连接", "可靠", "字节流", "全双工"], 2),
    kp("core_ch6_tcp_header", "TCP报文段首部", "概念", "传输层", "TCP首部至少20字节，包含端口、序号、确认号、标志位、窗口、检验和与选项等字段。", ["序号", "确认号", "标志位", "接收窗口"], 3),
    kp("core_ch6_seq_ack", "序号与确认号", "技术", "传输层", "TCP按字节编号；确认号表示期望收到的下一个字节序号，累积确认此前连续数据均已收到。", ["字节编号", "累计确认", "确认号", "有序交付"], 3),
    kp("core_ch6_handshake", "TCP三次握手", "技术", "传输层", "TCP以SYN、SYN+ACK、ACK三次报文交换同步双方初始序号并确认双向通信能力。", ["SYN", "ACK", "初始序号", "连接建立"], 3),
    kp("core_ch6_connection_release", "TCP四次挥手", "技术", "传输层", "TCP全双工连接的两个方向需分别关闭，典型过程为FIN、ACK、FIN、ACK。", ["FIN", "半关闭", "连接释放", "全双工"], 3),
    kp("core_ch6_time_wait", "TIME_WAIT状态", "概念", "传输层", "主动关闭方在最终ACK后保持TIME_WAIT，通常等待2MSL，以便重传最终ACK并让旧报文在网络中消失。", ["2MSL", "最终ACK", "旧报文", "主动关闭"], 4),
    kp("core_ch6_reliable", "可靠数据传输", "服务", "传输层", "可靠传输综合使用差错检测、序号、确认、定时器和重传，对上层呈现无差错且有序的数据流。", ["确认", "重传", "定时器", "有序交付"], 3),
    kp("core_ch6_checksum", "传输层检验和", "技术", "传输层", "检验和把报文按16位字进行反码求和，接收端据此发现传输中的比特差错，但不能纠错。", ["16位字", "反码", "差错检测", "伪首部"], 2),
    kp("core_ch6_stop_wait", "停止等待协议", "协议", "传输层", "停止等待协议每发送一个分组便等待确认，逻辑简单但在带宽时延积较大的链路上利用率低。", ["停止等待", "确认", "超时重传", "信道利用率"], 3),
    kp("core_ch6_pipelining", "流水线可靠传输", "技术", "传输层", "流水线允许多个未确认分组同时在途，通过扩大序号空间和缓存提高链路利用率。", ["流水线", "在途分组", "序号空间", "缓存"], 3),
    kp("core_ch6_sliding_window", "滑动窗口", "技术", "传输层", "滑动窗口限制发送方未确认数据范围，确认到达后窗口向前移动，实现流水线与发送速率约束。", ["发送窗口", "接收窗口", "累计确认", "窗口滑动"], 3),
    kp("core_ch6_flow_control", "TCP流量控制", "服务", "传输层", "接收方在首部中通告接收窗口rwnd，发送方限制未确认数据，避免接收缓存溢出。", ["rwnd", "接收缓存", "窗口通告", "零窗口"], 3),
    kp("core_ch6_rtt_rto", "RTT估计与重传超时", "算法", "传输层", "TCP以指数加权平均估计RTT，并结合RTT偏差设置RTO，使超时既能响应丢包又不过于敏感。", ["SampleRTT", "EstimatedRTT", "DevRTT", "RTO"], 4),
    kp("core_ch6_congestion", "TCP拥塞控制", "服务", "传输层", "TCP根据拥塞窗口cwnd和慢启动门限调节在途数据，以适应网络可用容量并避免拥塞崩溃。", ["cwnd", "ssthresh", "AIMD", "拥塞窗口"], 4),
    kp("core_ch6_slow_start", "慢开始", "算法", "传输层", "慢开始阶段每收到一个新的确认就增加cwnd，使拥塞窗口在每个RTT近似翻倍，直到门限或拥塞事件。", ["指数增长", "cwnd", "ssthresh", "RTT"], 3),
    kp("core_ch6_congestion_avoidance", "拥塞避免", "算法", "传输层", "拥塞避免采用加性增大，使cwnd每个RTT大约增加一个MSS，谨慎探测剩余带宽。", ["加性增大", "AIMD", "MSS", "线性增长"], 4),
    kp("core_ch6_fast_retransmit", "快重传", "算法", "传输层", "发送方收到三个重复ACK时，不等待超时便重传推测丢失的报文段，从而缩短丢包恢复时间。", ["三个重复ACK", "重传", "丢包", "无需超时"], 4),
    kp("core_ch6_fast_recovery", "快恢复", "算法", "传输层", "快恢复在重复ACK触发丢包后降低拥塞窗口但避免回到一个MSS，使连接较快恢复发送。", ["重复ACK", "门限", "窗口减小", "恢复"], 4),
    kp("core_ch6_tcp_udp_compare", "TCP与UDP对比", "概念", "传输层", "TCP强调连接、可靠性与拥塞控制；UDP强调报文边界、低时延和由应用自行控制可靠策略。", ["可靠性", "连接", "开销", "应用选择"], 2),
]


APPLICATION_NODES = [
    kp("core_ch7_application_layer", "应用层", "概念", "应用层", "应用层定义网络应用进程交换的报文类型、语义、格式和交互规则，直接为用户应用提供服务。", ["应用协议", "报文", "进程", "交互规则"], 1),
    kp("core_ch7_architecture", "网络应用体系结构", "概念", "应用层", "网络应用通常采用客户-服务器、对等或混合体系结构，体系结构决定进程组织和资源分布方式。", ["客户-服务器", "P2P", "进程组织", "体系结构"], 2),
    kp("core_ch7_client_server", "客户-服务器模式", "技术", "应用层", "客户进程主动请求服务，服务器在固定地址持续运行并响应多个客户，便于集中管理。", ["客户", "服务器", "请求响应", "固定地址"], 2),
    kp("core_ch7_p2p", "对等P2P模式", "技术", "应用层", "P2P中对等方既可请求也可提供资源，具有自扩展性，但管理、安全和可用性更复杂。", ["对等方", "自扩展", "去中心化", "资源共享"], 3),
    kp("core_ch7_socket_programming", "Socket编程", "技术", "应用层", "Socket API使应用选择TCP或UDP，通过地址和端口建立通信端点并执行发送、接收操作。", ["Socket API", "bind", "connect", "send/receive"], 3),
    kp("core_ch7_dns", "域名系统DNS", "服务", "应用层", "DNS是分布式、层次化命名系统，把域名解析为IP地址，并支持别名、邮件交换和负载分配。", ["域名解析", "分布式数据库", "53端口", "资源记录"], 2),
    kp("core_ch7_dns_hierarchy", "DNS层次结构", "概念", "应用层", "DNS由根域、顶级域和权威域名服务器形成层次结构，区域数据由相应权威服务器维护。", ["根服务器", "顶级域", "权威服务器", "区域"], 3),
    kp("core_ch7_dns_resolution", "递归与迭代解析", "技术", "应用层", "递归查询要求被询问服务器完成后续解析；迭代查询则返回下一步应询问的服务器地址。", ["递归查询", "迭代查询", "本地域名服务器", "转介"], 3),
    kp("core_ch7_dns_cache", "DNS缓存", "技术", "应用层", "解析器和域名服务器按TTL缓存资源记录，减少查询时延与根、顶级服务器负载。", ["TTL", "缓存命中", "过期", "查询时延"], 2),
    kp("core_ch7_dns_rr", "DNS资源记录", "概念", "应用层", "DNS资源记录以名称、值、类型和TTL表示，常见类型包括A、AAAA、NS、CNAME和MX。", ["A记录", "AAAA", "CNAME", "MX"], 3),
    kp("core_ch7_http", "HTTP协议", "协议", "应用层", "HTTP是Web的应用层协议，采用请求-响应模型，通常运行于TCP之上且本身无状态。", ["请求响应", "无状态", "Web", "TCP"], 2),
    kp("core_ch7_http_message", "HTTP报文", "概念", "应用层", "HTTP请求报文包含请求行、首部和可选实体；响应报文包含状态行、首部和可选实体。", ["请求行", "状态行", "首部", "实体"], 2),
    kp("core_ch7_persistent_http", "持续连接HTTP", "技术", "应用层", "持续连接允许同一TCP连接传输多个HTTP对象，减少重复握手开销和额外RTT。", ["持久连接", "RTT", "连接复用", "流水线"], 3),
    kp("core_ch7_cookie_session", "Cookie与会话", "技术", "应用层", "Cookie由服务器通过响应首部设置并由浏览器后续携带，配合服务端会话状态识别用户。", ["Set-Cookie", "Cookie", "会话标识", "状态管理"], 2),
    kp("core_ch7_web_cache", "Web缓存与代理", "服务", "应用层", "Web缓存保存可复用响应并代表客户向源服务器请求，能降低访问时延和出口链路流量。", ["代理服务器", "缓存命中", "条件GET", "访问时延"], 3),
    kp("core_ch7_https_tls", "HTTPS与TLS", "协议", "应用层", "HTTPS在HTTP与传输层之间使用TLS，提供服务器认证、机密性和报文完整性。", ["TLS", "证书", "加密", "完整性"], 3),
    kp("core_ch7_http2", "HTTP/2", "协议", "应用层", "HTTP/2在一个TCP连接中使用二进制分帧、多路复用和首部压缩，减少应用层队头等待。", ["二进制分帧", "多路复用", "HPACK", "单TCP连接"], 4),
    kp("core_ch7_http3", "HTTP/3", "协议", "应用层", "HTTP/3运行在基于UDP的QUIC之上，把可靠流和TLS 1.3结合，降低连接建立及跨流队头阻塞。", ["QUIC", "UDP", "TLS 1.3", "多流"], 4),
    kp("core_ch7_ftp", "FTP协议", "协议", "应用层", "FTP使用独立的控制连接和数据连接传输文件，控制连接通常使用TCP 21端口。", ["控制连接", "数据连接", "21端口", "文件传输"], 3),
    kp("core_ch7_email", "电子邮件系统", "服务", "应用层", "电子邮件系统由用户代理、邮件服务器和邮件传输协议组成，采用存储转发方式传递邮件。", ["用户代理", "邮件服务器", "存储转发", "消息队列"], 2),
    kp("core_ch7_smtp", "SMTP协议", "协议", "应用层", "SMTP用于邮件服务器之间以及客户端到服务器的邮件提交，基于TCP并采用命令-响应交互。", ["邮件发送", "TCP", "命令响应", "存储转发"], 2),
    kp("core_ch7_mime", "MIME", "协议", "应用层", "MIME扩展电子邮件格式，用Content-Type和编码方式承载非ASCII文本、图片与附件。", ["Content-Type", "附件", "编码", "多媒体邮件"], 3),
    kp("core_ch7_pop3", "POP3协议", "协议", "应用层", "POP3以下载并可删除服务器邮件为主要模式，功能简单，适合单一终端离线阅读。", ["邮件读取", "下载删除", "110端口", "离线"], 2),
    kp("core_ch7_imap", "IMAP协议", "协议", "应用层", "IMAP在服务器保留邮件和文件夹状态，支持多终端同步、服务器搜索与按需获取。", ["服务器存储", "多端同步", "文件夹", "按需获取"], 3),
    kp("core_ch7_dhcp", "DHCP协议", "协议", "应用层", "DHCP通过发现、提供、请求、确认过程动态分配IP地址、掩码、默认网关和DNS服务器。", ["DORA", "地址租约", "默认网关", "UDP"], 3),
    kp("core_ch7_url_uri", "URI与URL", "概念", "应用层", "URI统一标识资源，URL是URI的常见子集，说明访问资源所用方案、主机、端口与路径。", ["URI", "URL", "scheme", "资源定位"], 2),
    kp("core_ch7_websocket", "WebSocket协议", "协议", "应用层", "WebSocket先经HTTP Upgrade握手建立连接，随后在单一TCP连接上提供全双工消息通信。", ["Upgrade", "全双工", "长连接", "消息帧"], 3),
]


ALL_KNOWLEDGE_NODES = NETWORK_NODES + TRANSPORT_NODES + APPLICATION_NODES
ROOT_BY_CHAPTER = {
    "网络层": "core_ch5_network_layer",
    "传输层": "core_ch6_transport_layer",
    "应用层": "core_ch7_application_layer",
}


CALCULATIONS = {
    "core_ch5_ipv4_header": ("一个IPv4数据报总长度为1500字节，首部长度为20字节，其数据部分是多少字节？", "1480字节", "数据长度=总长度-首部长度=1500-20=1480字节。"),
    "core_ch5_subnet_mask": ("子网掩码255.255.255.192对应的CIDR前缀长度是多少？", "/26", "前三个字节有24个1，192的二进制为11000000，再有2个1，所以是/26。"),
    "core_ch5_subnetting": ("把一个/24地址块等长划分为/26子网，可得到多少个子网，每个子网有多少个可用主机地址？", "4个子网，每个62个可用主机地址", "借2位得到2^2=4个子网；保留网络地址和广播地址后，每网2^6-2=62个可用地址。"),
    "core_ch5_cidr": ("地址块192.168.10.0/24改按/27划分，可形成多少个等长子网？", "8个", "前缀增加3位，因此可形成2^3=8个/27子网。"),
    "core_ch5_ipv6": ("一个IPv6地址采用/64前缀，接口标识部分有多少位？", "64位", "IPv6地址共128位，接口标识长度为128-64=64位。"),
    "core_ch5_rip": ("RIP收到一条度量值为15跳的邻居路由后，加上到该邻居的一跳，新度量值是多少，含义是什么？", "16跳，表示不可达", "RIP把16作为无穷大；15+1=16，因此该目的网络不可达。"),
    "core_ch6_port": ("端口号字段为16位，理论上可表示多少个不同编号？", "65536个", "16位无符号数可表示2^16=65536个编号，即0到65535。"),
    "core_ch6_udp_header": ("UDP数据部分为512字节，UDP首部为8字节，UDP长度字段应填写多少？", "520字节", "UDP长度包含首部和数据，因此为8+512=520字节。"),
    "core_ch6_tcp_header": ("TCP首部数据偏移字段值为8时，首部长度是多少字节？", "32字节", "数据偏移以4字节为单位，8×4=32字节。"),
    "core_ch6_slow_start": ("慢开始时初始cwnd为1 MSS且无丢包，经过4个完整RTT后cwnd约为多少？", "16 MSS", "每个RTT近似翻倍：1→2→4→8→16 MSS。"),
    "core_ch6_stop_wait": ("停止等待协议发送时延1 ms、RTT为49 ms且忽略确认发送时延，发送方利用率约为多少？", "2%", "一个周期约为1+49=50 ms，利用率=1/50=2%。"),
    "core_ch7_dns_cache": ("某DNS记录TTL为600秒，缓存写入后第480秒收到查询，若记录未刷新还可使用多少秒？", "120秒", "剩余TTL=600-480=120秒。"),
    "core_ch7_persistent_http": ("忽略传输时间，非持续HTTP获取3个对象且每个对象新建TCP连接，每个对象约需2 RTT，共约多少RTT？", "6 RTT", "每个对象一次TCP握手RTT加一次请求响应RTT，3×2=6 RTT。"),
}


def first_sentence(text: str) -> str:
    return text.split("。", 1)[0] + "。"


def build_questions() -> list[dict[str, Any]]:
    by_chapter: dict[str, list[dict[str, Any]]] = {}
    for node in ALL_KNOWLEDGE_NODES:
        by_chapter.setdefault(node["chapter"], []).append(node)

    questions: list[dict[str, Any]] = []
    for index, node in enumerate(ALL_KNOWLEDGE_NODES):
        peers = [item for item in by_chapter[node["chapter"]] if item["id"] != node["id"]]
        rng = random.Random(node["id"])
        distractors = rng.sample(peers, 3)
        option_values = [(first_sentence(node["description"]), True)] + [
            (first_sentence(item["description"]), False) for item in distractors
        ]
        rng.shuffle(option_values)
        options = [f"{LETTERS[i]}. {value}" for i, (value, _) in enumerate(option_values)]
        answer = next(LETTERS[i] for i, (_, correct) in enumerate(option_values) if correct)
        drafts: list[tuple[str, str, list[str], str, str, int, str]] = [
            ("单选题", f"下列哪一项是对“{node['name']}”的准确表述？", options, answer,
             node["description"], 1, "易"),
            ("填空题", f"{first_sentence(node['description'])} 该知识点是________。", [], node["name"],
             f"题干给出的是“{node['name']}”的核心定义，关键词包括{'、'.join(node['keywords'][:3])}。", 3, "中"),
        ]
        if node["id"] in CALCULATIONS:
            title, calc_answer, explanation = CALCULATIONS[node["id"]]
            drafts.append(("计算题", title, [], calc_answer, explanation, 5, "难"))
        else:
            drafts.append(("简答题", f"请说明“{node['name']}”的主要作用，并列出至少两个关键特征。", [],
                           f"{node['description']} 关键特征：{'、'.join(node['keywords'][:4])}。",
                           f"答案应说明作用，并覆盖{'、'.join(node['keywords'][:2])}等要点。", 5, "难"))

        for sequence, (question_type, title, opts, q_answer, explanation, difficulty, label) in enumerate(drafts, 1):
            qid = f"core_q_{node['id'].removeprefix('core_')}_{sequence:02d}"
            questions.append({
                "id": qid,
                "name": f"{node['name']}·{question_type}",
                "question": title,
                "title": title,
                "type": question_type,
                "chapter": node["chapter"],
                "description": f"核心篇“{node['name']}”关联{question_type}。",
                "keywords": list(dict.fromkeys(node["keywords"] + [node["name"]]))[:6],
                "knowledge_point_id": node["id"],
                "related_nodes": [node["id"]],
                "options": opts,
                "answer": q_answer,
                "analysis": explanation,
                "explanation": explanation,
                "difficulty": difficulty,
                "difficulty_label": label,
            })
    return questions


def case(case_id: str, title: str, chapter: str, description: str, background: str,
         steps: list[str], related_nodes: list[str], analysis: str, tags: list[str]) -> dict[str, Any]:
    content = "\n".join([
        f"# {title}", "", "## 背景", background, "", "## 实施步骤",
        *[f"{i}. {step}" for i, step in enumerate(steps, 1)], "", "## 分析", analysis,
    ])
    return {
        "id": case_id,
        "title": title,
        "description": description,
        "background": background,
        "steps": steps,
        "related_nodes": related_nodes,
        "analysis": analysis,
        "chapter": chapter,
        "difficulty": 4,
        "content": content,
        "tags": tags,
        "image_urls": [],
        "video_url": None,
    }


CASES = [
    case("core_case_tcp_congestion", "TCP拥塞控制分析", "传输层", "根据cwnd、ssthresh和ACK序列识别慢开始、拥塞避免、快重传与快恢复。", "在可控网络中传输大文件并捕获TCP流，结合时间-序列图观察丢包前后的窗口变化。", ["使用Wireshark捕获单条TCP连接并导出序号、ACK和重传事件", "根据RTT分组绘制cwnd近似变化曲线", "区分超时与三个重复ACK两类拥塞信号", "计算新的ssthresh并解释恢复阶段"], ["core_ch6_tcp", "core_ch6_congestion", "core_ch6_slow_start", "core_ch6_congestion_avoidance", "core_ch6_fast_retransmit", "core_ch6_fast_recovery"], "cwnd在慢开始中近似按RTT指数增长，在拥塞避免中线性增长；超时通常导致更激进的窗口回退，重复ACK则允许快重传和快恢复。", ["TCP", "拥塞控制", "Wireshark", "cwnd"]),
    case("core_case_routing_simulation", "路由算法模拟", "网络层", "在同一拓扑上模拟距离向量与链路状态算法并比较收敛过程。", "构造五路由器加权拓扑，在链路故障前后观察各节点路由表变化。", ["建立带链路代价的邻接表", "运行Bellman-Ford式距离向量迭代并记录每轮结果", "泛洪链路状态后运行Dijkstra算法", "断开一条链路，比较收敛时间和路由环路风险"], ["core_ch5_routing_algorithm", "core_ch5_distance_vector", "core_ch5_link_state", "core_ch5_rip", "core_ch5_ospf"], "距离向量只依赖邻居信息，可能出现慢收敛和计数到无穷；链路状态需要维护全网拓扑，但通常能更快得到一致最短路径。", ["路由算法", "Bellman-Ford", "Dijkstra", "收敛"]),
    case("core_case_http_capture", "HTTP协议抓包分析", "应用层", "通过浏览器访问测试站点，分析HTTP请求、响应、状态码、首部与连接复用。", "使用浏览器开发者工具或Wireshark捕获一次页面加载，比较HTTP与HTTPS下可见信息。", ["清空浏览器缓存并开始抓包", "过滤HTTP或TCP流并定位GET请求", "检查Host、Cookie、Content-Type和缓存首部", "比较持续连接下多个对象的连接复用", "访问HTTPS站点并说明TLS加密后的可见边界"], ["core_ch7_http", "core_ch7_http_message", "core_ch7_persistent_http", "core_ch7_cookie_session", "core_ch7_https_tls"], "明文HTTP可直接观察请求行和首部；HTTPS只能看到TLS握手和加密记录。持续连接减少重复TCP握手，但HTTP/1.1仍可能受应用层队头等待影响。", ["HTTP", "抓包", "状态码", "TLS"]),
    case("core_case_dns_resolution", "DNS解析过程", "应用层", "跟踪从本地缓存到根、顶级域和权威服务器的完整域名解析链路。", "选择一个未缓存域名，使用nslookup或dig分别执行递归查询和迭代跟踪。", ["清理本地DNS缓存并记录配置的递归解析器", "查询A与AAAA记录并记录TTL", "使用迭代跟踪观察根、TLD和权威服务器转介", "重复查询比较缓存命中时延", "等待或推算TTL过期后的行为"], ["core_ch7_dns", "core_ch7_dns_hierarchy", "core_ch7_dns_resolution", "core_ch7_dns_cache", "core_ch7_dns_rr"], "客户端通常向本地解析器发递归请求，解析器再执行迭代查询。缓存显著降低时延，但TTL期间可能暂时返回尚未更新的记录。", ["DNS", "递归", "迭代", "TTL"]),
    case("core_case_tcp_lifecycle", "TCP三次握手与四次挥手", "传输层", "抓取完整TCP连接，逐项核对序号、确认号、标志位和TIME_WAIT。", "运行短连接客户端和服务器，保存从SYN到最终ACK的全部报文。", ["过滤指定TCP四元组", "标记SYN、SYN+ACK、ACK并验证确认号", "确认数据阶段序号按字节增长", "标记FIN与ACK并区分两个方向关闭", "在主动关闭端检查TIME_WAIT持续时间"], ["core_ch6_handshake", "core_ch6_seq_ack", "core_ch6_connection_release", "core_ch6_time_wait", "core_ch6_tcp_header"], "三次握手同步双方初始序号；四次挥手源于全双工两个方向独立关闭；TIME_WAIT保证最终ACK可重传并隔离旧连接报文。", ["三次握手", "四次挥手", "序号", "TIME_WAIT"]),
    case("core_case_subnetting", "子网划分计算", "网络层", "为部门网络分配VLSM地址块并验证网络地址、广播地址与可用主机范围。", "某单位获得192.168.10.0/24，需要为60、30、12台主机的三个部门分配互不重叠子网。", ["按主机需求从大到小排序", "为60台主机选择/26地址块", "为30台主机选择/27地址块", "为12台主机选择/28地址块", "计算每块网络地址、首末可用地址和广播地址", "用最长前缀匹配验证转发"], ["core_ch5_ipv4_addressing", "core_ch5_subnet_mask", "core_ch5_subnetting", "core_ch5_cidr", "core_ch5_longest_prefix"], "从大块开始分配可避免碎片。示例可依次使用192.168.10.0/26、192.168.10.64/27和192.168.10.96/28，剩余地址仍可继续划分。", ["子网划分", "VLSM", "CIDR", "广播地址"]),
    case("core_case_nat", "NAT工作原理", "网络层", "观察多台私网主机共享公网地址时地址与端口的转换表。", "两台内网主机同时访问同一Web服务器，边界路由器执行NAPT。", ["记录两台主机的私网四元组", "在内外接口同时抓取报文", "对比源IP与源端口变化", "建立并验证NAT映射表", "模拟映射超时后再次连接", "讨论入站连接和端到端原则限制"], ["core_ch5_nat", "core_ch5_ipv4_addressing", "core_ch5_router", "core_ch6_port", "core_ch6_socket"], "NAPT用不同公网端口区分内部连接。转换节省IPv4地址，但改变端到端可达性，入站服务通常需要静态映射或端口转发。", ["NAT", "NAPT", "端口映射", "私网"]),
    case("core_case_socket", "Socket编程实践", "应用层", "实现TCP回显与UDP查询程序，比较连接管理、报文边界和异常处理。", "使用Python标准socket库编写本地客户端与服务器，不依赖第三方网络框架。", ["实现TCP服务器的socket、bind、listen、accept流程", "实现TCP客户端connect并循环收发多条消息", "正确处理半包、粘包和连接关闭", "实现UDP服务器recvfrom与客户端sendto", "加入超时、日志和并发测试", "用抓包验证TCP字节流与UDP数据报边界"], ["core_ch7_socket_programming", "core_ch6_socket", "core_ch6_tcp", "core_ch6_udp", "core_ch6_multiplexing"], "TCP需要连接建立并提供可靠字节流，应用必须自行定义消息边界；UDP保留数据报边界但不保证到达。端口和地址共同把报文分用给正确进程。", ["Socket", "TCP", "UDP", "编程"]),
]


def edge(edge_id: str, source: str, target: str, relation: str, description: str) -> dict[str, str]:
    return {"id": edge_id, "source": source, "target": target, "relation": relation, "description": description}


def build_edges(questions: list[dict[str, Any]]) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    number = 1
    name_by_id = {node["id"]: node["name"] for node in ALL_KNOWLEDGE_NODES}

    def label(node_id: str) -> str:
        return name_by_id.get(node_id, node_id)

    def add(source: str, target: str, relation: str, description: str) -> None:
        nonlocal number
        edges.append(edge(f"core_edge_{number:04d}", source, target, relation, description))
        number += 1

    for node in ALL_KNOWLEDGE_NODES:
        root = ROOT_BY_CHAPTER[node["chapter"]]
        if node["id"] != root:
            add(node["id"], root, "属于层", f"{node['name']}属于{node['chapter']}")

    contains = {
        "core_ch5_ipv4": ["core_ch5_ipv4_header", "core_ch5_ipv4_addressing", "core_ch5_icmp"],
        "core_ch5_ipv4_addressing": ["core_ch5_classful_addressing", "core_ch5_subnet_mask", "core_ch5_subnetting", "core_ch5_cidr"],
        "core_ch5_routing_algorithm": ["core_ch5_distance_vector", "core_ch5_link_state"],
        "core_ch6_udp": ["core_ch6_udp_header", "core_ch6_udp_checksum"],
        "core_ch6_tcp": ["core_ch6_tcp_header", "core_ch6_seq_ack", "core_ch6_handshake", "core_ch6_connection_release", "core_ch6_reliable", "core_ch6_flow_control", "core_ch6_congestion"],
        "core_ch6_reliable": ["core_ch6_stop_wait", "core_ch6_pipelining", "core_ch6_sliding_window", "core_ch6_rtt_rto"],
        "core_ch6_congestion": ["core_ch6_slow_start", "core_ch6_congestion_avoidance", "core_ch6_fast_retransmit", "core_ch6_fast_recovery"],
        "core_ch7_dns": ["core_ch7_dns_hierarchy", "core_ch7_dns_resolution", "core_ch7_dns_cache", "core_ch7_dns_rr"],
        "core_ch7_http": ["core_ch7_http_message", "core_ch7_persistent_http", "core_ch7_cookie_session", "core_ch7_web_cache"],
        "core_ch7_email": ["core_ch7_smtp", "core_ch7_mime", "core_ch7_pop3", "core_ch7_imap"],
    }
    for parent, children in contains.items():
        for child in children:
            add(parent, child, "包含", f"{label(parent)}包含{label(child)}相关机制")

    prerequisites = [
        ("core_ch5_ipv4_addressing", "core_ch5_subnetting"), ("core_ch5_subnet_mask", "core_ch5_cidr"),
        ("core_ch5_forwarding_table", "core_ch5_longest_prefix"), ("core_ch5_routing_algorithm", "core_ch5_rip"),
        ("core_ch5_link_state", "core_ch5_ospf"), ("core_ch5_as", "core_ch5_bgp"),
        ("core_ch6_port", "core_ch6_multiplexing"), ("core_ch6_seq_ack", "core_ch6_reliable"),
        ("core_ch6_stop_wait", "core_ch6_pipelining"), ("core_ch6_sliding_window", "core_ch6_flow_control"),
        ("core_ch6_rtt_rto", "core_ch6_congestion"), ("core_ch7_architecture", "core_ch7_client_server"),
        ("core_ch7_architecture", "core_ch7_p2p"), ("core_ch7_dns_hierarchy", "core_ch7_dns_resolution"),
        ("core_ch7_http", "core_ch7_https_tls"), ("core_ch7_http", "core_ch7_http2"),
        ("core_ch7_http2", "core_ch7_http3"), ("core_ch7_email", "core_ch7_smtp"),
    ]
    for source, target in prerequisites:
        add(source, target, "前置知识", f"学习{label(target)}前应掌握{label(source)}")

    comparisons = [
        ("core_ch5_ipv4", "core_ch5_ipv6"), ("core_ch5_distance_vector", "core_ch5_link_state"),
        ("core_ch5_rip", "core_ch5_ospf"), ("core_ch6_tcp", "core_ch6_udp"),
        ("core_ch6_stop_wait", "core_ch6_sliding_window"), ("core_ch7_client_server", "core_ch7_p2p"),
        ("core_ch7_http", "core_ch7_https_tls"), ("core_ch7_pop3", "core_ch7_imap"),
    ]
    for source, target in comparisons:
        add(source, target, "对比", f"对比{label(source)}与{label(target)}的适用场景和机制")

    cross_edges = [
        ("core_ch5_ip_service", "core_ch6_transport_layer", "前置知识"),
        ("core_ch5_ipv4_addressing", "core_ch7_dns", "依赖"),
        ("core_ch6_tcp", "core_ch7_http", "应用于"), ("core_ch6_tcp", "core_ch7_https_tls", "应用于"),
        ("core_ch6_tcp", "core_ch7_ftp", "应用于"), ("core_ch6_tcp", "core_ch7_smtp", "应用于"),
        ("core_ch6_udp", "core_ch7_dns", "应用于"), ("core_ch6_udp", "core_ch7_dhcp", "应用于"),
        ("core_ch6_socket", "core_ch7_socket_programming", "前置知识"),
        ("core_ch5_nat", "core_ch6_port", "依赖"), ("core_ch7_http3", "core_ch6_udp", "依赖"),
    ]
    for source, target, relation in cross_edges:
        add(source, target, relation, f"核心篇跨章节关联：{label(source)}{relation}{label(target)}")

    for question in questions:
        node_id = question["knowledge_point_id"]
        add(node_id, question["id"], "关联试题", f"{label(node_id)}关联试题“{question['name']}”")
    for item in CASES:
        for node_id in item["related_nodes"]:
            add(node_id, item["id"], "相关案例", f"{node_id}关联案例“{item['title']}”")
    return edges


def question_nodes(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{
        "id": item["id"], "name": item["name"], "type": "问题", "layer": "问题层",
        "chapter": item["chapter"], "description": item["description"],
        "keywords": item["keywords"], "difficulty": item["difficulty"],
        "image_urls": [], "video_url": None,
    } for item in questions]


def case_nodes() -> list[dict[str, Any]]:
    return [{
        "id": item["id"], "name": item["title"], "type": "案例", "layer": "案例层",
        "chapter": item["chapter"], "description": item["description"],
        "keywords": item["tags"], "difficulty": item["difficulty"],
        "image_urls": item["image_urls"], "video_url": item["video_url"],
    } for item in CASES]


def read_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temporary.replace(path)


def validate(questions: list[dict[str, Any]], edges: list[dict[str, str]]) -> None:
    assert len(ALL_KNOWLEDGE_NODES) == 81
    assert len(NETWORK_NODES) == len(TRANSPORT_NODES) == len(APPLICATION_NODES) == 27
    assert len(questions) == 243
    assert len(CASES) == 8
    assert all(node["type"] in ALLOWED_NODE_TYPES for node in ALL_KNOWLEDGE_NODES)
    assert len({node["id"] for node in ALL_KNOWLEDGE_NODES}) == 81
    assert len({item["id"] for item in questions}) == 243
    assert len({item["id"] for item in CASES}) == 8
    coverage = Counter(item["knowledge_point_id"] for item in questions)
    assert set(coverage) == {node["id"] for node in ALL_KNOWLEDGE_NODES}
    assert set(coverage.values()) == {3}
    assert {item["type"] for item in questions} >= {"单选题", "填空题", "简答题", "计算题"}
    assert {item["difficulty_label"] for item in questions} == {"易", "中", "难"}
    all_ids = {node["id"] for node in ALL_KNOWLEDGE_NODES}
    all_ids.update(item["id"] for item in questions)
    all_ids.update(item["id"] for item in CASES)
    assert all(item["source"] in all_ids and item["target"] in all_ids for item in edges)
    assert {item["relation"] for item in edges} >= {"包含", "前置知识", "属于层", "相关案例", "关联试题", "应用于", "对比", "依赖"}


def merge_backend(questions: list[dict[str, Any]], edges: list[dict[str, str]]) -> None:
    nodes_path = BACKEND_DATA / "nodes.json"
    edges_path = BACKEND_DATA / "edges.json"
    questions_path = BACKEND_DATA / "questions.json"
    cases_path = BACKEND_DATA / "cases.json"
    old_nodes = read_json(nodes_path)
    removed_ids = {item["id"] for item in old_nodes if item.get("chapter") in CORE_CHAPTERS}
    merged_nodes = [item for item in old_nodes if item.get("chapter") not in CORE_CHAPTERS]
    merged_nodes += ALL_KNOWLEDGE_NODES + question_nodes(questions) + case_nodes()
    old_edges = read_json(edges_path)
    merged_edges = [item for item in old_edges if item.get("id", "").startswith("core_edge_") is False
                    and item.get("source") not in removed_ids and item.get("target") not in removed_ids]
    merged_edges += edges
    merged_questions = [item for item in read_json(questions_path) if item.get("chapter") not in CORE_CHAPTERS] + questions
    merged_cases = [item for item in read_json(cases_path) if item.get("chapter") not in CORE_CHAPTERS] + CASES
    write_json(nodes_path, merged_nodes)
    write_json(edges_path, merged_edges)
    write_json(questions_path, merged_questions)
    write_json(cases_path, merged_cases)


def main() -> None:
    questions = build_questions()
    edges = build_edges(questions)
    validate(questions, edges)
    write_json(CORE_DIR / "network_layer_nodes.json", NETWORK_NODES)
    write_json(CORE_DIR / "transport_layer_nodes.json", TRANSPORT_NODES)
    write_json(CORE_DIR / "application_layer_nodes.json", APPLICATION_NODES)
    write_json(CORE_DIR / "core_layer_edges.json", edges)
    write_json(CORE_DIR / "core_questions.json", questions)
    write_json(CORE_DIR / "core_cases.json", CASES)
    merge_backend(questions, edges)
    print(f"核心篇生成完成：知识点{len(ALL_KNOWLEDGE_NODES)}，关系{len(edges)}，试题{len(questions)}，案例{len(CASES)}。")


if __name__ == "__main__":
    main()
