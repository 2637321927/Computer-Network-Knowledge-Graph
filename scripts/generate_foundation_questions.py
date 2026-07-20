"""生成基础篇试题、问题层节点、关联边和可回溯记录。

本脚本只管理以下前缀，不覆盖其他成员的数据：
- 试题/问题节点：q_fd_
- 关联边：edge_qfd_
"""

from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "backend" / "data"
NODES_FILE = DATA_DIR / "nodes.json"
EDGES_FILE = DATA_DIR / "edges.json"
QUESTIONS_FILE = DATA_DIR / "questions.json"
FOUNDATION_TRACE_FILE = DATA_DIR / "foundation_traceability.json"
QUESTION_TRACE_FILE = DATA_DIR / "foundation_question_traceability.json"

QUESTION_PREFIX = "q_fd_"
EDGE_PREFIX = "edge_qfd_"
FOUNDATION_PREFIXES = ("ch1_", "ch2_", "ch3_", "ch4_")
LETTERS = "ABCD"

EXPECTED_CHAPTER_COUNTS = {
    "计算机网络概述": 60,
    "物理层": 72,
    "数据链路层": 54,
    "局域网原理": 72,
}
EXPECTED_TYPE_COUNTS = {
    "单选题": 90,
    "多选题": 36,
    "判断题": 42,
    "填空题": 30,
    "简答题": 36,
    "计算题": 24,
}


CALCULATION_QUESTIONS: dict[str, dict[str, Any]] = {
    "ch1_packet_switching": {
        "title": "一条消息被划分为100个等长分组，每个分组12,000 bit，依次经过两条速率均为6 Mbps的链路。采用存储转发和流水传输，忽略传播、处理、排队时延及首部开销，发送完整消息至少需要多长时间？",
        "answer": "202 ms",
        "explanation": "每个分组在一条链路上的发送时延为12000÷(6×10^6)=2 ms。100个分组通过2条链路的流水总时间为(2+100-1)×2=202 ms。",
        "related_nodes": ["ch1_packet_switching", "ch1_store_and_forward"],
    },
    "ch1_store_and_forward": {
        "title": "一个12,000 bit的分组经过3条速率均为6 Mbps的链路，采用存储转发。三条链路的传播时延之和为15 ms，忽略处理和排队时延，求端到端时延。",
        "answer": "21 ms",
        "explanation": "每条链路的发送时延为12000÷(6×10^6)=2 ms，3条链路共6 ms；加上传播时延15 ms，总时延为21 ms。",
        "related_nodes": ["ch1_store_and_forward", "ch1_nodal_delay"],
    },
    "ch1_circuit_switching": {
        "title": "一条2 Mbps链路采用同步TDM为20个用户平均分配时隙。忽略开销，每个用户获得的固定传输速率是多少？",
        "answer": "100 kbps",
        "explanation": "同步TDM平均分配链路容量，每个用户速率为2 Mbps÷20=0.1 Mbps=100 kbps。",
        "related_nodes": ["ch1_circuit_switching", "ch2_tdm"],
    },
    "ch1_nodal_delay": {
        "title": "某分组在一个结点的处理时延为1 ms、排队时延为4 ms。分组长12,000 bit，链路速率6 Mbps；链路长2,000 km，传播速率2×10^8 m/s。求该结点总时延。",
        "answer": "17 ms",
        "explanation": "传输时延为2 ms，传播时延为2000 km÷(2×10^8 m/s)=10 ms，所以总时延为1+4+2+10=17 ms。",
        "related_nodes": ["ch1_nodal_delay", "ch1_store_and_forward"],
    },
    "ch1_traffic_intensity": {
        "title": "平均分组长度L=12,000 bit，平均到达率a=500 packet/s，输出链路速率R=10 Mbps。计算流量强度La/R，并判断队列是否处于长期过载状态。",
        "answer": "La/R=0.6，未处于长期过载状态",
        "explanation": "La/R=12000×500÷10,000,000=0.6，小于1，平均到达工作量没有超过链路服务能力。",
        "related_nodes": ["ch1_traffic_intensity", "ch1_queueing_packet_loss"],
    },
    "ch1_throughput_bottleneck": {
        "title": "一条端到端连接依次经过40 Mbps接入链路、由4条连接公平共享的120 Mbps核心链路，以及50 Mbps接收链路。该连接可获得的端到端吞吐量是多少？",
        "answer": "30 Mbps",
        "explanation": "核心链路中每条连接分得120÷4=30 Mbps。端到端吞吐量取40、30、50 Mbps中的最小值，因此为30 Mbps。",
        "related_nodes": ["ch1_throughput_bottleneck", "ch1_network_core"],
    },
    "ch2_qam": {
        "title": "某通信系统采用64-QAM，码元速率为2,400 Baud。忽略编码开销，理论比特率是多少？",
        "answer": "14.4 kbps",
        "explanation": "64个星座点可表示log2(64)=6 bit/码元，所以比特率为2400×6=14,400 bit/s。",
        "related_nodes": ["ch2_qam", "ch2_bandpass_modulation"],
    },
    "ch2_nyquist_criterion": {
        "title": "理想低通信道带宽为3 kHz，采用16种离散信号状态。根据奈奎斯特公式，最高数据传输速率是多少？",
        "answer": "24 kbps",
        "explanation": "最高码元速率为2W，数据率为2Wlog2(M)=2×3000×log2(16)=24,000 bit/s。",
        "related_nodes": ["ch2_nyquist_criterion", "ch2_channel_distortion"],
    },
    "ch2_snr": {
        "title": "某信道的信噪比为30 dB，求线性信噪比S/N。",
        "answer": "S/N=1000",
        "explanation": "由30=10log10(S/N)，得到S/N=10^(30/10)=1000。",
        "related_nodes": ["ch2_snr"],
    },
    "ch2_shannon_capacity": {
        "title": "某信道带宽为3 kHz，信噪比为30 dB。根据香农公式计算理论极限容量。",
        "answer": "约29.9 kbps",
        "explanation": "30 dB对应S/N=1000，C=3000×log2(1+1000)≈29,902 bit/s，约为29.9 kbps。",
        "related_nodes": ["ch2_shannon_capacity", "ch2_snr"],
    },
    "ch2_fdm": {
        "title": "FDM系统为5个用户各分配20 kHz子频带，相邻子频带之间设置2 kHz保护带。整个系统至少需要多大总带宽？",
        "answer": "108 kHz",
        "explanation": "5个用户频带共5×20=100 kHz，5个子频带之间有4个保护间隔，共4×2=8 kHz，总计108 kHz。",
        "related_nodes": ["ch2_fdm", "ch2_multiplexing"],
    },
    "ch2_tdm": {
        "title": "同步TDM复用4路64 kbps数字信号，每帧给每路分配1 bit且忽略同步开销。复用链路速率和每帧持续时间分别是多少？",
        "answer": "256 kbps；15.625 μs",
        "explanation": "复用速率为4×64=256 kbps。每路每帧发送1 bit，为保持64 kbit/s，每秒需64,000帧，帧时长为1/64000 s=15.625 μs。",
        "related_nodes": ["ch2_tdm", "ch2_multiplexing"],
    },
    "ch2_cdm": {
        "title": "某CDM站点码片序列S=(-1,-1,-1,+1,+1,-1,+1,+1)，接收的合成信号恰好为-S。接收信号与S的规格化内积是多少？该站发送的是比特0还是1？",
        "answer": "规格化内积为-1，发送比特0",
        "explanation": "(-S)·S除以码片数等于-1。CDM约定S表示比特1，-S表示比特0。",
        "related_nodes": ["ch2_cdm"],
    },
    "ch2_dmt": {
        "title": "某DMT系统有256个有效子信道，每个子信道每个码元承载15 bit，码元率均为4,000 Baud。若协议开销占10%，有效数据率是多少？",
        "answer": "13.824 Mbps",
        "explanation": "原始速率为256×15×4000=15.36 Mbps，扣除10%开销后为15.36×0.9=13.824 Mbps。",
        "related_nodes": ["ch2_dmt", "ch2_adsl"],
    },
    "ch3_crc": {
        "title": "待发送数据D=1101011011，生成多项式对应序列G=1011。求CRC余数R。",
        "answer": "100",
        "explanation": "G为4 bit，先在D后补3个0，再以1011作模二除法，得到3 bit余数100。",
        "related_nodes": ["ch3_crc", "ch3_error_detection"],
    },
    "ch3_ideal_mac": {
        "title": "一条100 Mbps广播链路上有4个节点持续发送。按照理想MAC协议的公平性目标，每个节点平均应获得多少速率？",
        "answer": "25 Mbps",
        "explanation": "理想MAC在M个活跃节点之间平均分配速率R，因此每个节点获得R/M=100÷4=25 Mbps。",
        "related_nodes": ["ch3_ideal_mac", "ch3_multiple_access_link"],
    },
    "ch3_slotted_aloha": {
        "title": "时隙ALOHA的总尝试负载G=1。使用S=G×e^(-G)计算吞吐率，并说明它是否达到理论最大值。",
        "answer": "S=1/e≈0.368，达到理论最大值",
        "explanation": "代入G=1得S=e^(-1)≈0.368。时隙ALOHA在G=1时达到最大吞吐率，约37%。",
        "related_nodes": ["ch3_slotted_aloha"],
    },
    "ch3_pure_aloha": {
        "title": "纯ALOHA的总尝试负载G=0.5。使用S=G×e^(-2G)计算吞吐率，并说明它是否达到理论最大值。",
        "answer": "S=0.5/e≈0.184，达到理论最大值",
        "explanation": "代入G=0.5得S=0.5e^(-1)≈0.184。纯ALOHA在G=0.5时达到最大吞吐率，约18%。",
        "related_nodes": ["ch3_pure_aloha"],
    },
    "ch3_csma_cd": {
        "title": "某CSMA/CD总线网络速率为100 Mbps，最大单向传播时延为25 μs。为了检测最远端冲突，帧至少应有多少比特和多少字节？",
        "answer": "5000 bit，即625 byte",
        "explanation": "帧发送时间至少等于往返传播时延，Lmin=2×25 μs×100 Mbps=5000 bit=625 byte。",
        "related_nodes": ["ch3_csma_cd"],
    },
    "ch3_binary_exponential_backoff": {
        "title": "10 Mbps以太网中，某站经历第4次碰撞。按二进制指数退避算法，K的选择范围是什么？若随机变量均匀分布，平均退避时间是多少？",
        "answer": "K∈[0,15]；平均退避时间0.384 ms",
        "explanation": "第4次碰撞后K从0到2^4-1中选择，平均K为7.5。一个bit time为0.1 μs，因此平均退避为7.5×512×0.1 μs=384 μs=0.384 ms。",
        "related_nodes": ["ch3_binary_exponential_backoff", "ch3_csma_cd"],
    },
    "ch4_mac_address": {
        "title": "标准MAC地址长度为48 bit。它占多少字节？理论上共有多少种不同取值？",
        "answer": "6 byte；2^48种",
        "explanation": "8 bit为1 byte，所以48 bit=6 byte；48个二进制位理论上可组成2^48个不同地址。",
        "related_nodes": ["ch4_mac_address"],
    },
    "ch4_ethernet_frame": {
        "title": "一个以太网帧的数据字段为100 byte。忽略前导码和帧间间隔，只计算目的MAC、源MAC、类型、数据和CRC，帧长是多少？",
        "answer": "118 byte",
        "explanation": "帧长为6+6+2+100+4=118 byte。100 byte数据大于最小数据字段，不需要额外填充。",
        "related_nodes": ["ch4_ethernet_frame"],
    },
    "ch4_collision_domain": {
        "title": "12台主机分别通过独立全双工链路接入一台交换机的12个端口。按端口链路划分，共有多少个独立碰撞域？正常全双工通信中会发生多少次CSMA/CD碰撞？",
        "answer": "12个独立碰撞域；正常情况下0次碰撞",
        "explanation": "交换机的每条端口链路构成独立碰撞域；全双工链路没有共享介质竞争，因此不使用CSMA/CD且不会发生碰撞。",
        "related_nodes": ["ch4_collision_domain", "ch4_ethernet_switch"],
    },
    "ch4_vlan_trunk_8021q": {
        "title": "802.1Q标签中的VLAN ID字段为12 bit。理论上可表示多少个编号？扣除0和4095两个保留值后，常规可用VLAN ID有多少个？",
        "answer": "理论4096个；常规可用4094个",
        "explanation": "12 bit可表示2^12=4096个编号；0和4095保留，因此常规可用编号为1～4094，共4094个。",
        "related_nodes": ["ch4_vlan_trunk_8021q", "ch4_vlan"],
    },
}


SOURCE_CATALOG = {
    "local_scope": {
        "description": "课程PPT决定范围，个人Markdown笔记决定中文表述与知识密度。",
        "trace_file": "backend/data/foundation_traceability.json",
    },
    "kurose_interactive": {
        "description": "Kurose/Ross官方交互练习；用于时延、吞吐量、CRC、ALOHA和交换机题型设计。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/interactive/",
    },
    "ncre_sample": {
        "description": "中国教育考试网四级计算机网络样题；用于中文单选、多选题的表述方式校核。",
        "url": "https://ncre.neea.edu.cn/res/Home/2501/2351319548cf65dfc6cd8ba95cf1f8e2.pdf",
    },
    "kurose_knowledge_checks": {
        "description": "Kurose/Ross官方知识检查；用于概念辨析和基础计算题型设计。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=4",
    },
    "kurose_link_layer": {
        "description": "Kurose/Ross官方链路层资源；用于链路层、ARP、以太网和VLAN覆盖检查。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/videos/6/",
    },
    "kurose_wireshark": {
        "description": "Kurose/Ross官方Wireshark实验；用于以太网帧与ARP场景题设计。",
        "url": "https://gaia.cs.umass.edu/kurose_ross/wireshark.php/interactive/interactive/interactive/",
    },
    "rfc826": {
        "description": "ARP规范依据。",
        "url": "https://datatracker.ietf.org/doc/html/rfc826",
    },
    "umaine_ethernet": {
        "description": "University of Maine ECE435有线以太网作业；用于帧解析与设备输出场景题型设计。",
        "url": "https://web.eece.maine.edu/~vweaver/classes/ece435_2025s/ece435_hw10.pdf",
    },
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


def reference_basis(node_id: str) -> list[str]:
    """按章节和主题记录实际用于题型、机制校核的公开依据。"""
    basis = ["local_scope", "ncre_sample"]
    if node_id.startswith("ch1_"):
        basis.extend(["kurose_interactive", "kurose_knowledge_checks"])
    elif node_id.startswith("ch2_"):
        basis.extend(["kurose_interactive", "kurose_knowledge_checks"])
    elif node_id.startswith("ch3_"):
        basis.extend(["kurose_interactive", "kurose_link_layer"])
    elif node_id.startswith("ch4_"):
        basis.extend(["kurose_link_layer", "kurose_wireshark"])
        if any(term in node_id for term in ("ethernet", "switch", "collision")):
            basis.append("umaine_ethernet")
        if "arp" in node_id or node_id == "ch4_cross_subnet_delivery":
            basis.append("rfc826")
    return basis


def first_sentence(text: str) -> str:
    for marker in ("。", "！", "？"):
        if marker in text:
            return text.split(marker, 1)[0] + marker
    return text


def shuffled_options(values: list[tuple[str, bool]], seed: str) -> tuple[list[str], str]:
    rng = random.Random(seed)
    rng.shuffle(values)
    options = [f"{LETTERS[i]}. {value}" for i, (value, _) in enumerate(values)]
    answer = "".join(LETTERS[i] for i, (_, correct) in enumerate(values) if correct)
    return options, answer


def distractor_nodes(node: dict[str, Any], chapter_nodes: list[dict[str, Any]], count: int) -> list[dict[str, Any]]:
    candidates = [item for item in chapter_nodes if item["id"] != node["id"]]
    rng = random.Random(node["id"] + f":distractors:{count}")
    rng.shuffle(candidates)
    return candidates[:count]


def make_identification_question(node: dict[str, Any], chapter_nodes: list[dict[str, Any]]) -> dict[str, Any]:
    alternatives = distractor_nodes(node, chapter_nodes, 3)
    values = [(first_sentence(node["description"]), True)] + [
        (first_sentence(item["description"]), False) for item in alternatives
    ]
    options, answer = shuffled_options(values, node["id"] + ":identify")
    return {
        "title": f"下列关于“{node['name']}”的表述，正确的是：",
        "type": "单选题",
        "options": options,
        "answer": answer,
        "explanation": node["description"],
        "difficulty": max(1, min(3, node["difficulty"])),
    }


def make_secondary_question(
    node: dict[str, Any], chapter_nodes: list[dict[str, Any]], question_type: str, index: int
) -> dict[str, Any]:
    other_nodes = distractor_nodes(node, chapter_nodes, 4)
    keywords = list(dict.fromkeys(node.get("keywords", [])))

    if question_type == "单选题":
        correct = keywords[0] if keywords else node["name"]
        wrong = [item.get("keywords", [item["name"]])[0] for item in other_nodes[:3]]
        options, answer = shuffled_options(
            [(correct, True)] + [(item, False) for item in wrong], node["id"] + ":keyword-single"
        )
        return {
            "title": f"下列哪一项与“{node['name']}”的关系最直接？",
            "type": "单选题",
            "options": options,
            "answer": answer,
            "explanation": f"“{correct}”是该知识点的核心关键词。{node['description']}",
        }

    if question_type == "多选题":
        correct_items = keywords[:2] if len(keywords) >= 2 else [node["name"], first_sentence(node["description"])]
        wrong_items: list[str] = []
        for item in other_nodes:
            for keyword in item.get("keywords", [item["name"]]):
                if keyword not in correct_items and keyword not in wrong_items:
                    wrong_items.append(keyword)
                    break
            if len(wrong_items) == 2:
                break
        options, answer = shuffled_options(
            [(item, True) for item in correct_items[:2]] + [(item, False) for item in wrong_items[:2]],
            node["id"] + ":multi",
        )
        return {
            "title": f"下列哪些术语或特征与“{node['name']}”直接相关？",
            "type": "多选题",
            "options": options,
            "answer": answer,
            "explanation": f"直接相关的关键词是“{'、'.join(correct_items[:2])}”。{node['description']}",
        }

    if question_type == "判断题":
        is_true = index % 2 == 0
        if is_true:
            statement = first_sentence(node["description"])
            answer = "正确"
        else:
            other = other_nodes[0]
            statement = f"“{node['name']}”的核心含义是：{first_sentence(other['description'])}"
            answer = "错误"
        return {
            "title": statement,
            "type": "判断题",
            "options": ["正确", "错误"],
            "answer": answer,
            "explanation": node["description"],
        }

    return {
        "title": f"“________”是指：{first_sentence(node['description'])}",
        "type": "填空题",
        "options": [],
        "answer": node["name"],
        "explanation": node["description"],
    }


def make_tertiary_question(node: dict[str, Any], question_type: str) -> dict[str, Any]:
    if question_type == "计算题":
        result = dict(CALCULATION_QUESTIONS[node["id"]])
        result["type"] = "计算题"
        result["options"] = []
        result["difficulty"] = max(3, node["difficulty"])
        return result

    if question_type == "填空题":
        keywords = node.get("keywords", [])
        for keyword in keywords:
            if keyword and keyword in node["description"] and keyword != node["name"]:
                statement = first_sentence(node["description"]).replace(keyword, "________", 1)
                return {
                    "title": statement,
                    "type": "填空题",
                    "options": [],
                    "answer": keyword,
                    "explanation": node["description"],
                    "difficulty": max(2, node["difficulty"]),
                }
        return {
            "title": f"“________”是指：{first_sentence(node['description'])}",
            "type": "填空题",
            "options": [],
            "answer": node["name"],
            "explanation": node["description"],
            "difficulty": max(2, node["difficulty"]),
        }

    return {
        "title": f"请简述“{node['name']}”的核心含义，并说明它描述或解决的主要问题。",
        "type": "简答题",
        "options": [],
        "answer": node["description"],
        "explanation": f"答案应覆盖这些要点：{'、'.join(node.get('keywords', []))}。",
        "difficulty": max(2, node["difficulty"]),
    }


def secondary_type(index: int) -> str:
    if index < 4:
        return "单选题"
    if index < 40:
        return "多选题"
    if index < 82:
        return "判断题"
    return "填空题"


def build_questions(foundation_nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_chapter: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in foundation_nodes:
        by_chapter[node["chapter"]].append(node)

    non_calculation_ids = [node["id"] for node in foundation_nodes if node["id"] not in CALCULATION_QUESTIONS]
    fill_ids = set(non_calculation_ids[:26])
    generated: list[dict[str, Any]] = []

    for index, node in enumerate(foundation_nodes):
        chapter_nodes = by_chapter[node["chapter"]]
        drafts = [
            make_identification_question(node, chapter_nodes),
            make_secondary_question(node, chapter_nodes, secondary_type(index), index),
            make_tertiary_question(
                node,
                "计算题" if node["id"] in CALCULATION_QUESTIONS else ("填空题" if node["id"] in fill_ids else "简答题"),
            ),
        ]

        for sequence, draft in enumerate(drafts, start=1):
            question_id = f"{QUESTION_PREFIX}{node['id']}_{sequence:02d}"
            related_nodes = draft.pop("related_nodes", [node["id"]])
            generated.append(
                {
                    "id": question_id,
                    "name": f"{node['name']}·基础题{sequence}",
                    "title": draft["title"],
                    "type": draft["type"],
                    "chapter": node["chapter"],
                    "description": f"基础篇“{node['name']}”知识点的{draft['type']}。",
                    "keywords": list(dict.fromkeys(node.get("keywords", []) + [node["name"]]))[:6],
                    "related_nodes": related_nodes,
                    "options": draft.get("options", []),
                    "answer": draft["answer"],
                    "explanation": draft["explanation"],
                    "difficulty": draft.get("difficulty", max(1, min(5, node["difficulty"]))),
                }
            )
    return generated


def validate_questions(questions: list[dict[str, Any]], foundation_nodes: list[dict[str, Any]]) -> None:
    ids = [item["id"] for item in questions]
    if len(ids) != len(set(ids)):
        raise ValueError("基础篇试题ID重复")
    if len(questions) != 258:
        raise ValueError(f"基础篇试题应为258道，实际为{len(questions)}道")

    chapter_counts = Counter(item["chapter"] for item in questions)
    if dict(chapter_counts) != EXPECTED_CHAPTER_COUNTS:
        raise ValueError(f"章节题量不正确：{dict(chapter_counts)}")
    type_counts = Counter(item["type"] for item in questions)
    if dict(type_counts) != EXPECTED_TYPE_COUNTS:
        raise ValueError(f"题型数量不正确：{dict(type_counts)}")

    expected_node_ids = {item["id"] for item in foundation_nodes}
    coverage = Counter(
        related
        for item in questions
        for related in item["related_nodes"]
        if related in expected_node_ids and related == item["id"].removeprefix(QUESTION_PREFIX).rsplit("_", 1)[0]
    )
    missing = sorted(expected_node_ids - set(coverage))
    wrong_count = {node_id: count for node_id, count in coverage.items() if count != 3}
    if missing or wrong_count:
        raise ValueError(f"知识点覆盖不完整：missing={missing}, wrong_count={wrong_count}")

    for item in questions:
        if not item["title"] or not item["answer"] or not item["explanation"]:
            raise ValueError(f"题干、答案或解析为空：{item['id']}")
        if item["type"] in {"单选题", "多选题"} and len(item["options"]) != 4:
            raise ValueError(f"选择题选项数不是4：{item['id']}")
        if not 1 <= item["difficulty"] <= 5:
            raise ValueError(f"难度越界：{item['id']}")


def main() -> None:
    all_nodes = read_json(NODES_FILE)
    all_edges = read_json(EDGES_FILE)
    all_questions = read_json(QUESTIONS_FILE)
    foundation_trace = read_json(FOUNDATION_TRACE_FILE)

    foundation_nodes = [item for item in all_nodes if item["id"].startswith(FOUNDATION_PREFIXES)]
    if len(foundation_nodes) != 86:
        raise ValueError(f"基础篇知识点应为86个，实际为{len(foundation_nodes)}个")

    generated_questions = build_questions(foundation_nodes)
    validate_questions(generated_questions, foundation_nodes)

    preserved_questions = [item for item in all_questions if not item.get("id", "").startswith(QUESTION_PREFIX)]
    merged_questions = preserved_questions + generated_questions

    preserved_nodes = [item for item in all_nodes if not item.get("id", "").startswith(QUESTION_PREFIX)]
    question_nodes = [
        {
            "id": item["id"],
            "name": item["name"],
            "type": "问题",
            "layer": "问题层",
            "chapter": item["chapter"],
            "description": item["description"],
            "keywords": item["keywords"],
            "difficulty": item["difficulty"],
            "image_urls": [],
            "video_url": None,
        }
        for item in generated_questions
    ]
    merged_nodes = preserved_nodes + question_nodes

    preserved_edges = [item for item in all_edges if not item.get("id", "").startswith(EDGE_PREFIX)]
    question_edges = []
    edge_number = 1
    for question in generated_questions:
        for related_node in question["related_nodes"]:
            question_edges.append(
                {
                    "id": f"{EDGE_PREFIX}{edge_number:04d}",
                    "source": related_node,
                    "target": question["id"],
                    "relation": "关联试题",
                    "description": f"“{related_node}”关联基础篇试题“{question['name']}”",
                }
            )
            edge_number += 1
    merged_edges = preserved_edges + question_edges

    all_node_ids = {item["id"] for item in merged_nodes}
    dangling = [
        item["id"] for item in merged_edges
        if item["source"] not in all_node_ids or item["target"] not in all_node_ids
    ]
    if dangling:
        raise ValueError(f"存在悬空关系：{dangling}")

    node_trace = foundation_trace.get("nodes", {})
    trace_questions = {}
    for question in generated_questions:
        primary_node = question["id"].removeprefix(QUESTION_PREFIX).rsplit("_", 1)[0]
        trace_questions[question["id"]] = {
            "primary_node": primary_node,
            "related_nodes": question["related_nodes"],
            "question_type": question["type"],
            "origin": "依据课程范围原创编写；公开资源只用于题型与事实校核，未直接复制题干。",
            "local_evidence": node_trace.get(primary_node, {}),
            "reference_basis": reference_basis(primary_node),
        }

    trace_payload = {
        "scope": "基础篇试题：计算机网络概述、物理层、数据链路层、局域网原理",
        "generation": {
            "script": "scripts/generate_foundation_questions.py",
            "managed_question_prefix": QUESTION_PREFIX,
            "managed_edge_prefix": EDGE_PREFIX,
            "knowledge_node_count": len(foundation_nodes),
            "questions_per_knowledge_node": 3,
            "question_count": len(generated_questions),
            "question_node_count": len(question_nodes),
            "question_edge_count": len(question_edges),
            "chapter_counts": dict(Counter(item["chapter"] for item in generated_questions)),
            "type_counts": dict(Counter(item["type"] for item in generated_questions)),
        },
        "source_catalog": SOURCE_CATALOG,
        "questions": trace_questions,
    }

    write_json_atomic(QUESTIONS_FILE, merged_questions)
    write_json_atomic(NODES_FILE, merged_nodes)
    write_json_atomic(EDGES_FILE, merged_edges)
    write_json_atomic(QUESTION_TRACE_FILE, trace_payload)
    print(
        f"基础篇试题生成完成：{len(generated_questions)}道试题，"
        f"{len(question_nodes)}个问题层节点，{len(question_edges)}条关联边。"
    )
    print(f"章节分布：{dict(Counter(item['chapter'] for item in generated_questions))}")
    print(f"题型分布：{dict(Counter(item['type'] for item in generated_questions))}")


if __name__ == "__main__":
    main()
