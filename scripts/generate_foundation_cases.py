"""生成基础篇案例、案例层节点、相关案例边和可回溯记录。

本脚本只管理以下前缀，不覆盖其他成员的数据：
- 案例/案例节点：case_fd_
- 案例关系：edge_cfd_
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from textwrap import dedent
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "backend" / "data"
NODES_FILE = DATA_DIR / "nodes.json"
EDGES_FILE = DATA_DIR / "edges.json"
CASES_FILE = DATA_DIR / "cases.json"
FOUNDATION_TRACE_FILE = DATA_DIR / "foundation_traceability.json"
CASE_TRACE_FILE = DATA_DIR / "foundation_case_traceability.json"

CASE_PREFIX = "case_fd_"
EDGE_PREFIX = "edge_cfd_"


SOURCE_CATALOG = {
    "local_scope": {
        "description": "课程PPT决定范围，个人Markdown笔记决定中文表述与知识密度。",
        "trace_file": "backend/data/foundation_traceability.json",
    },
    "kurose_delay": {
        "description": "Kurose/Ross官方时延与吞吐量知识检查。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=4",
    },
    "njit_line_coding": {
        "description": "NJIT ECE489线路编码实验。",
        "url": "https://web.njit.edu/~gilhc/ECE489/ece489-XI.htm",
    },
    "etsu_line_coding": {
        "description": "ETSU开放课程：极性与双极性线路编码。",
        "url": "https://dc.etsu.edu/computer-organization-design-oer/27/",
    },
    "uf_transmission": {
        "description": "University of Florida计算机网络物理层传输资料。",
        "url": "https://www.cise.ufl.edu/~nemo/cen4500/transmission.html",
    },
    "bucknell_design": {
        "description": "Bucknell University数字通信系统设计练习。",
        "url": "https://www.eg.bucknell.edu/~kozick/elec470/digdes.html",
    },
    "kurose_crc": {
        "description": "Kurose/Ross官方CRC交互练习。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/interactive/CRC.php",
    },
    "kurose_aloha": {
        "description": "Kurose/Ross官方ALOHA交互练习。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/interactive/aloha.php",
    },
    "kurose_wireshark": {
        "description": "Kurose/Ross官方Wireshark Ethernet与ARP实验。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/wireshark.php/interactive/interactive/interactive/",
    },
    "rfc826": {
        "description": "ARP协议规范。",
        "url": "https://datatracker.ietf.org/doc/html/rfc826",
    },
    "kurose_switch": {
        "description": "Kurose/Ross官方自学习交换机交互练习。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/interactive/learning_switch_basic.php",
    },
    "cisco_switching": {
        "description": "Cisco LAN交换环境与转发、过滤、泛洪排障资料。",
        "url": "https://www.cisco.com/c/en/us/support/docs/lan-switching/ethernet/12006-chapter22.html",
    },
    "cisco_trunk_lab": {
        "description": "Cisco Networking Academy Packet Tracer Trunk实验。",
        "url": "https://www.netacad.com/content/srwe/1.0/courses/content/m3/en-US/assets/3.4.5-packet-tracer---configure-trunks.pdf",
    },
}


CASES: list[dict[str, Any]] = [
    {
        "id": "case_fd_ch1_delay_bottleneck",
        "title": "校园网视频下载变慢：时延、排队与瓶颈分析",
        "description": "通过校园网多用户同时下载视频的场景，计算结点时延、流量强度和共享瓶颈吞吐量，并比较分组交换与电路交换。",
        "chapter": "计算机网络概述",
        "difficulty": 3,
        "related_nodes": [
            "ch1_packet_switching",
            "ch1_queueing_packet_loss",
            "ch1_circuit_switching",
            "ch1_nodal_delay",
            "ch1_traffic_intensity",
            "ch1_throughput_bottleneck",
        ],
        "tags": ["端到端时延", "排队", "流量强度", "瓶颈链路", "分组交换"],
        "sources": ["local_scope", "kurose_delay"],
        "content": dedent(
            """
            # 校园网视频下载变慢

            四名学生同时通过校园网下载视频。大家看到的现象是：刚开始还能播放，人数一多就开始缓冲，严重时还会出现丢包。这个案例要把“网速慢”拆成时延、排队和吞吐量三个问题。

            ## 网络条件

            ```text
            客户端 --100 Mbps接入链路-- 校园边缘路由器
                   --20 Mbps共享核心链路-- 服务器侧路由器
                   --200 Mbps服务器链路-- 视频服务器
            ```

            - 分组长度：`L=12,000 bit`
            - 三段链路传播时延之和：`12 ms`
            - 路由器处理时延之和：`2 ms`
            - 核心链路开始发送前已有5个等长分组排队
            - 核心链路由4条视频连接公平共享

            ## 任务一：算出第一个分组的时延

            三条链路的传输时延分别为：

            ```text
            12,000 / 100 Mbps = 0.12 ms
            12,000 / 20 Mbps  = 0.60 ms
            12,000 / 200 Mbps = 0.06 ms
            ```

            核心链路前有5个分组，所以排队时延近似为：

            ```text
            5 × 0.60 ms = 3 ms
            ```

            结点总时延近似为：

            ```text
            d = 0.12 + 0.60 + 0.06 + 3 + 12 + 2
              = 17.78 ms
            ```

            注意：传输时延由`L/R`决定，传播时延由距离和信号传播速度决定，两者不是一回事。

            ## 任务二：判断队列负载

            如果核心链路平均每秒到达1,400个分组：

            ```text
            La/R = 12,000 × 1,400 / 20,000,000 = 0.84
            ```

            `La/R`还小于1，但已经比较接近1，平均排队时延会明显增大。如果到达率上升到1,800 packet/s：

            ```text
            La/R = 1.08
            ```

            这时长期到达工作量超过服务能力，队列会持续增长，缓冲区最终溢出并丢包。

            ## 任务三：找瓶颈吞吐量

            4条连接公平共享20 Mbps核心链路，每条连接最多分到：

            ```text
            20 Mbps / 4 = 5 Mbps
            ```

            端到端吞吐量取路径上可用速率的最小值，所以每名学生约为5 Mbps。即使服务器链路提高到1 Gbps，只要20 Mbps共享核心链路不变，用户吞吐量仍不会提高。

            ## 分组交换还是电路交换

            如果为每个用户预留5 Mbps电路，4个用户会占满20 Mbps。用户暂停视频时，预留带宽也不能立即给其他用户使用。分组交换允许突发业务按需共享资源，利用率更高，但代价是高负载下会出现排队、时延和丢包。

            ## 结论

            - “网页打开慢”不一定是传播距离远，也可能是排队造成的。
            - `La/R`接近1时，排队时延会迅速增加。
            - 端到端吞吐量由瓶颈链路决定。
            - 提升非瓶颈链路速率通常不能解决问题。

            """
        ).strip(),
    },
    {
        "id": "case_fd_ch2_line_coding_sync",
        "title": "长串比特传输失败：线路编码与时钟同步",
        "description": "对同一比特串分别采用NRZ、曼彻斯特和差分曼彻斯特编码，分析长时间无跳变造成的同步问题以及带宽代价。",
        "chapter": "物理层",
        "difficulty": 3,
        "related_nodes": [
            "ch2_data_signal_system",
            "ch2_baseband_signal_modulation",
            "ch2_line_coding",
            "ch2_channel_distortion",
        ],
        "tags": ["线路编码", "NRZ", "曼彻斯特", "自同步", "波形"],
        "sources": ["local_scope", "njit_line_coding", "etsu_line_coding"],
        "content": dedent(
            """
            # 长串比特传输失败

            发送端连续发送`00000000101101`。使用NRZ编码时，接收端在前8个0期间很久都看不到电平跳变，时钟稍有偏差就可能把一个bit判断成两个，或者漏掉一个bit。

            ## 实验约定

            为避免不同教材的0、1电平约定不同，本案例统一规定：

            - NRZ-L：`1`为高电平，`0`为低电平。
            - 曼彻斯特：`1`为码元中间低到高跳变，`0`为中间高到低跳变。
            - 差分曼彻斯特：每个码元中间一定跳变；码元开始处有跳变表示`0`，无跳变表示`1`。

            ## 操作步骤

            1. 画出时间轴，每个bit划分为前半和后半两个区间。
            2. 分别画出NRZ-L、曼彻斯特和差分曼彻斯特波形。
            3. 假设接收端时钟每个bit慢1%，观察连续8个0后采样点的位置偏移。
            4. 把整条线路的正负极性反转，再对三种波形解码。
            5. 统计每种编码在一个bit时间内可能出现的最大跳变次数。

            ## 观察结果

            **NRZ-L**：连续0期间电平保持不变。接收端只能依赖自己的本地时钟划分bit边界，长串相同比特容易积累同步误差。

            **曼彻斯特编码**：每个bit中间都有一次固定跳变，接收端能从跳变中恢复时钟，因此具有自同步能力。但一个bit至少需要两个信号区间，频谱需求比NRZ高。

            **差分曼彻斯特编码**：信息由“相邻码元边界是否跳变”表示，而不是由绝对高低电平表示。线路极性整体反转后，跳变关系不变，因此仍能正确解码。

            ## 故障判断

            如果抓到的波形长时间保持同一电平，而接收数据在长串0或1后开始错位，优先考虑：

            - 编码本身缺少同步跳变；
            - 收发时钟存在频率偏差；
            - 信道失真使跳变边沿变得不清楚；
            - 码元速率过高，产生码间串扰。

            ## 结论

            线路编码不是简单地把0换成低电平、1换成高电平。编码还要考虑同步、直流分量、抗极性反转能力和带宽。曼彻斯特类编码用更多跳变换取可靠同步。

            """
        ).strip(),
    },
    {
        "id": "case_fd_ch2_adsl_capacity",
        "title": "ADSL线路速率下降：信噪比与信道容量评估",
        "description": "根据带宽和不同距离下的信噪比计算奈奎斯特与香农上限，解释ADSL速率随距离下降以及DMT自适应分配的作用。",
        "chapter": "物理层",
        "difficulty": 4,
        "related_nodes": [
            "ch2_snr",
            "ch2_shannon_capacity",
            "ch2_nyquist_criterion",
            "ch2_guided_media",
            "ch2_adsl",
            "ch2_dmt",
            "ch2_fttx",
        ],
        "tags": ["ADSL", "DMT", "信噪比", "香农容量", "奈奎斯特"],
        "sources": ["local_scope", "uf_transmission", "bucknell_design"],
        "content": dedent(
            """
            # ADSL线路速率为什么随距离下降

            同一套餐的两个用户使用相同电话线接入。近端用户测得信噪比30 dB，远端用户只有20 dB。假设可用带宽均为1.1 MHz，运营商希望提供8 Mbps下行速率。

            ## 第一步：把dB换成线性信噪比

            ```text
            SNR(dB) = 10 log10(S/N)
            ```

            - 30 dB对应`S/N=1000`。
            - 20 dB对应`S/N=100`。

            ## 第二步：计算香农容量

            ```text
            C = W log2(1 + S/N)
            ```

            近端线路：

            ```text
            C = 1.1×10^6 × log2(1001) ≈ 10.96 Mbps
            ```

            远端线路：

            ```text
            C = 1.1×10^6 × log2(101) ≈ 7.32 Mbps
            ```

            8 Mbps低于近端线路的香农上限，理论上可能实现；但它已经超过远端线路的7.32 Mbps理论上限，再好的调制器也不能保证无差错达到8 Mbps。

            ## 第三步：用奈奎斯特准则检查码元方案

            如果每个码元有16种状态，每个码元携带4 bit：

            ```text
            Rmax = 2W log2(16)
                 = 2 × 1.1 MHz × 4
                 = 8.8 Mbps
            ```

            8.8 Mbps是假设理想无噪声信道得到的上限。实际设计还必须同时满足香农容量，因此远端线路仍不能达到8 Mbps。

            ## DMT怎样处理不同质量的子信道

            DMT把ADSL高频频谱划分为许多窄子信道。训练阶段分别测量每个子信道质量：

            - 信噪比高的子信道分配更多bit；
            - 信噪比一般的子信道分配较少bit；
            - 干扰严重的子信道可以暂时停用；
            - 线路条件变化时重新调整bit分配。

            远端用户的铜线更长，衰减和外部干扰更明显，可用子信道和每个子信道能够承载的bit都会减少，所以同步速率下降。

            ## 方案比较

            - 继续使用ADSL：复用现有电话线，成本低，但速率受距离和铜线质量影响。
            - 改用FTTx：光纤损耗小、容量大且不受电磁干扰，适合更高带宽需求。

            ## 结论

            奈奎斯特准则描述理想带宽限制，香农公式进一步考虑噪声。实际速率不能超过两类限制中更严格的一项。ADSL使用DMT不是突破香农上限，而是尽量逼近不同子信道条件下的可用容量。

            """
        ).strip(),
    },
    {
        "id": "case_fd_ch3_crc_burst_error",
        "title": "传输途中发生突发差错：CRC检测实验",
        "description": "对给定数据完成CRC编码，分别注入单比特和突发错误，并在接收端通过模二除法判断帧是否出错。",
        "chapter": "数据链路层",
        "difficulty": 4,
        "related_nodes": ["ch3_frame", "ch3_error_detection", "ch3_parity", "ch3_crc"],
        "tags": ["CRC", "模二除法", "突发差错", "奇偶校验", "差错检测"],
        "sources": ["local_scope", "kurose_crc"],
        "content": dedent(
            """
            # CRC突发差错检测实验

            发送端准备发送数据：

            ```text
            D = 1101011011
            G = 1011
            ```

            `G`有4 bit，所以CRC余数长度`r=3`。

            ## 发送端计算

            先在数据D后补3个0：

            ```text
            1101011011000
            ```

            使用`1011`进行模二除法。模二减法就是按位异或，不需要借位。得到余数：

            ```text
            R = 100
            ```

            最终发送比特串为：

            ```text
            D || R = 1101011011100
            ```

            正确比特串可以被`G`整除，接收端余数应为`000`。

            ## 注入错误

            分别进行三次实验：

            1. 翻转发送串中的一个bit。
            2. 连续翻转3个bit，模拟短突发干扰。
            3. 不改变比特串，作为对照组。

            每次都把接收串重新除以`G`：

            - 余数为`000`：没有检测到错误；
            - 余数不为`000`：检测到帧发生错误，应丢弃或交给上层恢复。

            ## 与奇偶校验比较

            一维奇偶校验能够检测奇数个bit翻转，但偶数个bit同时翻转可能逃过检查。二维奇偶校验能够定位并纠正单bit错误。CRC通过选择生成多项式，可以有效检测多类突发错误，能力通常强于简单奇偶校验。

            ## 注意

            CRC的作用是**检测错误**，不是自动恢复原始数据。并且差错检测并非百分之百可靠，某些错误模式可能恰好仍能被生成多项式整除。

            ## 结论

            发送端增加EDC会带来少量开销，但能让接收端在不了解原始数据的情况下检查帧是否受到破坏。生成多项式的选择决定了CRC能够检测哪些错误模式。

            """
        ).strip(),
    },
    {
        "id": "case_fd_ch3_shared_channel_collision",
        "title": "多台主机同时发送：从ALOHA到CSMA/CD",
        "description": "通过共享总线上的发送时间表比较纯ALOHA、时隙ALOHA和CSMA/CD，并计算最小帧长与二进制指数退避范围。",
        "chapter": "数据链路层",
        "difficulty": 4,
        "related_nodes": [
            "ch3_multiple_access_link",
            "ch3_mac_taxonomy",
            "ch3_slotted_aloha",
            "ch3_pure_aloha",
            "ch3_csma",
            "ch3_csma_cd",
            "ch3_binary_exponential_backoff",
        ],
        "tags": ["ALOHA", "CSMA", "CSMA/CD", "碰撞", "指数退避"],
        "sources": ["local_scope", "kurose_aloha"],
        "content": dedent(
            """
            # 多台主机同时发送

            4台主机共享一条广播链路，每个frame恰好占用一个时隙。某5个时隙中的发送情况如下：

            | 时隙 | 尝试发送的主机 | 结果 |
            | --- | --- | --- |
            | 0 | A、B | 碰撞 |
            | 1 | C | 成功 |
            | 2 | A | 成功 |
            | 3 | B、D | 碰撞 |
            | 4 | D | 成功 |

            这个短序列的成功率是`3/5=60%`，但它只是一次样本，不代表协议长期理论效率。

            ## 纯ALOHA与时隙ALOHA

            **纯ALOHA**中，节点有帧就立即发送。一个frame发送时间为T，只要其他节点在前后共`2T`的脆弱期内开始发送，就可能重叠冲突。理论最大效率约为：

            ```text
            1 / (2e) ≈ 18%
            ```

            **时隙ALOHA**要求所有节点只在时隙开始发送，把脆弱期缩短为T。理论最大效率约为：

            ```text
            1 / e ≈ 37%
            ```

            冲突后不能所有节点立刻同时重传，否则还会再次碰撞，所以每个节点以概率`p`决定是否在下一时隙重传。

            ## 为什么CSMA仍会碰撞

            CSMA发送前先侦听信道。但信号传播需要时间：A刚开始发送时，远端B还没听到A的信号，也可能判断信道空闲并开始发送，所以“先听后发”不能彻底消除碰撞。

            ## CSMA/CD最小帧长

            假设链路速率`R=100 Mbps`，最大单向传播时延`τ=20 μs`。为了让发送端在最坏情况下仍能检测到碰撞：

            ```text
            Lmin / R >= 2τ
            Lmin >= 2 × 20 μs × 100 Mbps
                 = 4,000 bit
                 = 500 byte
            ```

            如果帧太短，发送端可能已经发送结束才收到远端碰撞信号，便会误以为发送成功。

            ## 二进制指数退避

            发生第3次碰撞后：

            ```text
            K ∈ {0,1,2,3,4,5,6,7}
            等待时间 = K × 512 bit times
            ```

            碰撞次数越多，随机等待范围越大，让高负载下的节点逐渐分散重传时间。

            ## 结论

            - ALOHA直接竞争，简单但效率较低。
            - CSMA利用载波侦听减少碰撞，但传播时延使碰撞仍可能发生。
            - CSMA/CD通过边发边检测快速停止失败发送。
            - 指数退避在低负载时等待较短，高负载时扩大随机范围。

            """
        ).strip(),
    },
    {
        "id": "case_fd_ch4_wireshark_arp",
        "title": "Wireshark捕获Ethernet与ARP报文",
        "description": "通过清理ARP缓存并执行ping，捕获广播ARP请求、单播ARP回复和以太网帧，比较同子网与跨子网交付。",
        "chapter": "局域网原理",
        "difficulty": 3,
        "related_nodes": [
            "ch4_mac_address",
            "ch4_arp",
            "ch4_arp_table",
            "ch4_cross_subnet_delivery",
            "ch4_ethernet_frame",
        ],
        "tags": ["Wireshark", "ARP", "Ethernet", "MAC地址", "抓包"],
        "sources": ["local_scope", "kurose_wireshark", "rfc826"],
        "content": dedent(
            """
            # Wireshark捕获Ethernet与ARP报文

            主机发送IP datagram前，必须先知道这一跳应该填写哪个目的MAC地址。这个实验直接观察ARP请求、ARP回复以及随后发送的以太网帧。

            ## 实验准备

            1. 使用`ipconfig`查看本机IPv4地址、子网掩码和默认网关。
            2. 使用`arp -a`记录当前ARP缓存。
            3. 在权限允许时删除目标IP对应的ARP表项；如果无法删除，可以换一个近期没有通信过的同子网目标。
            4. 打开Wireshark，选择正在联网的网卡开始捕获。

            ## 捕获同子网通信

            对同一子网中的另一台主机执行：

            ```text
            ping <同子网主机IP>
            ```

            使用显示过滤器：

            ```text
            arp
            ```

            应观察到：

            - ARP request封装在广播以太网帧中，目的MAC为`FF:FF:FF:FF:FF:FF`；
            - 请求内容的意思是“谁拥有这个IP，请告诉发送者”；
            - 目标主机发送ARP reply，通常使用单播回复；
            - 本机ARP表增加目标IP与MAC地址的映射；
            - 后续IP datagram的以太网目的MAC是目标主机MAC。

            ## 捕获跨子网通信

            再ping一个不同子网的IP，例如公共DNS地址。IP datagram中的目的IP仍然是远端主机，但本机这一跳的以太网目的MAC不是远端服务器MAC，而是默认网关接口的MAC。

            ```text
            端到端IP目的地址：远端服务器IP
            第一跳Ethernet目的地址：默认网关MAC
            ```

            路由器收到frame后去掉旧链路层首部，再根据下一跳重新封装。IP地址负责端到端寻址，MAC地址负责当前链路上的一跳交付。

            ## 检查以太网字段

            选择一个以太网帧，查看：

            - Destination：目的MAC；
            - Source：源MAC；
            - Type：上层协议类型；
            - Payload：通常是IP datagram或ARP报文。

            注意：很多网卡在硬件中生成或校验FCS，操作系统抓包时不一定把FCS交给Wireshark。因此看不到CRC字段不等于线上没有FCS。

            ## 结论

            ARP只解析同一链路中的下一跳MAC。ARP请求使用广播，是因为发送者此时还不知道目标接口在哪里；ARP回复能够单播，是因为请求中已经携带发送者的MAC地址。

            """
        ).strip(),
    },
    {
        "id": "case_fd_ch4_switch_learning",
        "title": "交换机为什么先泛洪后定向转发",
        "description": "在两台交换机转发表初始为空的条件下，逐帧推导源MAC学习、未知目的泛洪、已知目的转发和同端口过滤。",
        "chapter": "局域网原理",
        "difficulty": 3,
        "related_nodes": [
            "ch4_ethernet_switch",
            "ch4_switch_table",
            "ch4_switch_self_learning",
            "ch4_switch_filter_forward",
            "ch4_switch_interconnection",
        ],
        "tags": ["交换机", "自学习", "转发表", "泛洪", "过滤"],
        "sources": ["local_scope", "kurose_switch", "cisco_switching"],
        "content": dedent(
            """
            # 交换机为什么先泛洪后定向转发

            两台交换机刚启动时转发表为空，但主机不需要手工告诉交换机自己在哪个端口。交换机通过收到frame时的源MAC自动学习。

            ## 拓扑

            ```text
            A -- S1端口1          S2端口1 -- C
            B -- S1端口2 --端口5/5-- S2端口2 -- D
            ```

            S1与S2通过各自端口5相连。开始时两张转发表都为空。

            ## 第一次通信：A发送给C

            1. S1从端口1收到frame，学习`A -> 端口1`。
            2. S1不知道C的位置，所以除端口1外向端口2和端口5泛洪。
            3. S2从端口5收到frame，学习`A -> 端口5`。
            4. S2不知道C的位置，所以向端口1和端口2泛洪。
            5. C接收frame，B和D发现目的MAC不是自己后丢弃。

            ## C回复A

            1. S2从端口1收到回复，学习`C -> 端口1`。
            2. S2已经知道A位于端口5，只向端口5定向转发。
            3. S1从端口5收到回复，学习`C -> 端口5`。
            4. S1已经知道A位于端口1，只向端口1转发。

            经过一次请求和回复，两台交换机就学习到了A和C的位置，后续通信不再泛洪到无关端口。

            ## B发送给A

            S1从端口2收到frame，先学习`B -> 端口2`。目的A已知，所以只向端口1转发，frame不会经过交换机间链路。

            如果A和B都位于同一外接集线器一侧，交换机收到B发给A的frame后发现目的端口与来向端口相同，就会过滤，不再从该端口发回去。

            ## 表项超时

            转发表项带有时间戳。A长时间不发送后，`A -> 端口1`可能被删除。此时C再次发给A，目的MAC重新变为未知，交换机会再次泛洪；A一回复，交换机又能重新学习。

            ## 转发规则

            ```text
            收到frame：永远先根据源MAC学习
            目的MAC已知且出口不同：定向转发
            目的MAC已知且出口等于来向：过滤
            目的MAC未知：除来向接口外泛洪
            ```

            """
        ).strip(),
    },
    {
        "id": "case_fd_ch4_vlan_trunk",
        "title": "同VLAN主机无法跨交换机通信：802.1Q Trunk排障",
        "description": "在Packet Tracer中排查跨交换机同VLAN通信失败，完成Access端口、Trunk、允许VLAN和Native VLAN配置。",
        "chapter": "局域网原理",
        "difficulty": 4,
        "related_nodes": [
            "ch4_ethernet_frame",
            "ch4_switch_interconnection",
            "ch4_vlan",
            "ch4_port_based_vlan",
            "ch4_vlan_trunk_8021q",
        ],
        "tags": ["VLAN", "Trunk", "802.1Q", "Packet Tracer", "故障排查"],
        "sources": ["local_scope", "cisco_trunk_lab"],
        "content": dedent(
            """
            # 同VLAN主机无法跨交换机通信

            两台交换机上都配置了VLAN 10和VLAN 20。同一台交换机内、同一VLAN的主机可以通信，但跨交换机后，即使两台主机属于同一VLAN也无法ping通。

            ## 拓扑与地址

            ```text
            PC1(VLAN10, 192.168.10.11) -- S1 -- S2 -- PC3(VLAN10, 192.168.10.12)
            PC2(VLAN20, 192.168.20.11) -- S1 -- S2 -- PC4(VLAN20, 192.168.20.12)
            ```

            初始故障：S1和S2之间的接口仍是默认Access端口，属于VLAN 1，不能承载VLAN 10和VLAN 20的带标签流量。

            ## 第一步：检查Access端口

            ```text
            show vlan brief
            ```

            在两台交换机上创建VLAN并分配主机端口：

            ```text
            vlan 10
             name STUDENT
            vlan 20
             name TEACHER
            vlan 99
             name NATIVE

            interface f0/2
             switchport mode access
             switchport access vlan 10

            interface f0/3
             switchport mode access
             switchport access vlan 20
            ```

            ## 第二步：配置交换机间Trunk

            假设两台交换机使用`f0/1`互联，两端都配置：

            ```text
            interface f0/1
             switchport mode trunk
             switchport trunk native vlan 99
             switchport trunk allowed vlan 10,20,99
            ```

            使用下面的命令验证：

            ```text
            show interfaces trunk
            ```

            应确认接口处于trunking状态，Native VLAN均为99，允许列表中包含10、20和99。

            ## 第三步：分层测试

            1. PC1 ping PC3：同属VLAN 10，应当成功。
            2. PC2 ping PC4：同属VLAN 20，应当成功。
            3. PC1 ping PC2：属于不同VLAN，在没有路由器或三层交换功能时应失败。

            VLAN划分的是广播域。Trunk让同一VLAN跨越多台交换机，但不会自动提供不同VLAN之间的通信。

            ## 常见故障

            - 一端是Trunk，另一端仍为Access；
            - Trunk允许列表漏掉目标VLAN；
            - 两端Native VLAN不同；
            - 主机端口被分到错误VLAN；
            - 某台交换机没有创建对应VLAN。

            ## 802.1Q标签

            Trunk上的frame需要携带VLAN ID，让接收交换机知道frame属于哪个逻辑LAN。802.1Q标签改变了frame内容，所以发送端必须重新计算CRC。Native VLAN流量通常不带标签，两端Native VLAN不一致会导致流量被归入错误广播域。

            """
        ).strip(),
    },
]


EXPECTED_CHAPTER_COUNTS = {
    "计算机网络概述": 1,
    "物理层": 2,
    "数据链路层": 2,
    "局域网原理": 3,
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json_atomic(path: Path, payload: Any) -> None:
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temp_path.replace(path)


def validate_cases(cases: list[dict[str, Any]], all_node_ids: set[str]) -> None:
    if len(cases) != 8:
        raise ValueError(f"基础篇案例应为8个，实际为{len(cases)}个")
    ids = [item["id"] for item in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("基础篇案例ID重复")
    chapter_counts = dict(Counter(item["chapter"] for item in cases))
    if chapter_counts != EXPECTED_CHAPTER_COUNTS:
        raise ValueError(f"章节案例数不正确：{chapter_counts}")

    required = {"id", "title", "description", "chapter", "difficulty", "related_nodes", "content", "tags"}
    for item in cases:
        missing_fields = [field for field in required if not item.get(field)]
        if missing_fields:
            raise ValueError(f"案例字段为空：{item['id']} -> {missing_fields}")
        if not 1 <= item["difficulty"] <= 5:
            raise ValueError(f"案例难度越界：{item['id']}")
        missing_nodes = [node_id for node_id in item["related_nodes"] if node_id not in all_node_ids]
        if missing_nodes:
            raise ValueError(f"案例关联不存在的知识点：{item['id']} -> {missing_nodes}")
        if len(item["content"]) < 500:
            raise ValueError(f"案例正文过短：{item['id']}")


def main() -> None:
    all_nodes = read_json(NODES_FILE)
    all_edges = read_json(EDGES_FILE)
    all_cases = read_json(CASES_FILE)
    foundation_trace = read_json(FOUNDATION_TRACE_FILE)
    all_node_ids_before = {item["id"] for item in all_nodes}

    validate_cases(CASES, all_node_ids_before)

    preserved_cases = [item for item in all_cases if not item.get("id", "").startswith(CASE_PREFIX)]
    stored_cases = [
        {
            key: value
            for key, value in item.items()
            if key not in {"sources"}
        }
        | {"image_urls": [], "video_url": None}
        for item in CASES
    ]
    merged_cases = preserved_cases + stored_cases

    preserved_nodes = [item for item in all_nodes if not item.get("id", "").startswith(CASE_PREFIX)]
    case_nodes = [
        {
            "id": item["id"],
            "name": item["title"],
            "type": "案例",
            "layer": "案例层",
            "chapter": item["chapter"],
            "description": item["description"],
            "keywords": item["tags"],
            "difficulty": item["difficulty"],
            "image_urls": [],
            "video_url": None,
        }
        for item in CASES
    ]
    merged_nodes = preserved_nodes + case_nodes

    preserved_edges = [item for item in all_edges if not item.get("id", "").startswith(EDGE_PREFIX)]
    case_edges = []
    edge_number = 1
    for case in CASES:
        for related_node in case["related_nodes"]:
            case_edges.append(
                {
                    "id": f"{EDGE_PREFIX}{edge_number:03d}",
                    "source": related_node,
                    "target": case["id"],
                    "relation": "相关案例",
                    "description": f"“{related_node}”在案例“{case['title']}”中得到应用",
                }
            )
            edge_number += 1
    merged_edges = preserved_edges + case_edges

    all_node_ids = {item["id"] for item in merged_nodes}
    edge_ids = [item["id"] for item in merged_edges]
    if len(edge_ids) != len(set(edge_ids)):
        raise ValueError("合并后的关系ID重复")
    dangling = [
        item["id"] for item in merged_edges
        if item["source"] not in all_node_ids or item["target"] not in all_node_ids
    ]
    if dangling:
        raise ValueError(f"存在悬空案例关系：{dangling}")

    node_trace = foundation_trace.get("nodes", {})
    trace_cases = {}
    for case in CASES:
        local_evidence = {}
        for node_id in case["related_nodes"]:
            local_evidence[node_id] = node_trace.get(node_id, {})
        trace_cases[case["id"]] = {
            "title": case["title"],
            "chapter": case["chapter"],
            "related_nodes": case["related_nodes"],
            "origin": "依据课程范围原创编写；公开资料用于案例形式和机制校核，未直接复制案例正文。",
            "local_evidence": local_evidence,
            "reference_basis": case["sources"],
        }

    trace_payload = {
        "scope": "基础篇案例：计算机网络概述、物理层、数据链路层、局域网原理",
        "pdf_requirement": "案例库建议覆盖不少于20个典型网络问题；基础篇按4/10章比例贡献8个案例。",
        "generation": {
            "script": "scripts/generate_foundation_cases.py",
            "managed_case_prefix": CASE_PREFIX,
            "managed_edge_prefix": EDGE_PREFIX,
            "case_count": len(CASES),
            "case_node_count": len(case_nodes),
            "case_edge_count": len(case_edges),
            "chapter_counts": dict(Counter(item["chapter"] for item in CASES)),
        },
        "source_catalog": SOURCE_CATALOG,
        "cases": trace_cases,
    }

    write_json_atomic(CASES_FILE, merged_cases)
    write_json_atomic(NODES_FILE, merged_nodes)
    write_json_atomic(EDGES_FILE, merged_edges)
    write_json_atomic(CASE_TRACE_FILE, trace_payload)
    print(
        f"基础篇案例生成完成：{len(CASES)}个案例，"
        f"{len(case_nodes)}个案例层节点，{len(case_edges)}条相关案例边。"
    )
    print(f"章节分布：{dict(Counter(item['chapter'] for item in CASES))}")


if __name__ == "__main__":
    main()
