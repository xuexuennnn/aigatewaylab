# -*- coding: utf-8 -*-
"""简体中文页面文案（/zh/ 树）。独立撰写，不逐句对照英文；
结构、锚点与诚实性规则与英文树保持一致。"""

HOME_TITLE = "自托管 AI API 网关：部署与运维"
HOME_DESC = ("面向团队的自托管 AI API 网关部署、加固与运维服务：Docker、HTTPS、"
             "密钥治理、监控告警、备份恢复与故障转移。独立演示站。")
HOME_BODY = """
<div class="hero">
<div>
<p class="kicker">部署 &middot; 加固 &middot; 运维</p>
<h1>自托管 AI API 网关<br>部署与运维</h1>
<p class="lead">为需要统一管理 LLM 流量入口的团队提供网关部署、安全加固与
长期运维支持。密钥、日志、基础设施，全部掌握在你自己手里。</p>
<p class="cta-row">
  <a class="btn contact-mail" href="mailto:hello@aigatewaylab.xyz?subject=Gateway%20deployment%20review">申请部署评估</a>
  <a class="btn ghost btn-gap" href="demo/">查看在线演示</a>
</p>
<p class="contact-plain dim">邮箱：<span class="contact-addr">hello@aigatewaylab.xyz</span>
<span class="copy-hint" aria-live="polite"></span></p>
</div>
<div class="hero-console" aria-label="部署流程示意（静态示例）">
  <div class="hc-bar"><span class="hc-dot"></span><span class="hc-dot"></span><span class="hc-dot"></span>部署 &middot; 验证 &middot; 交接</div>
<pre><code><span class="hc-c"># 每一次交付，都以验证数据收尾</span>
<span class="hc-k">$</span> deployctl preflight --remote gateway-host
<span class="hc-o">ok</span>  80/443 空闲 &middot; docker 27.x &middot; 磁盘余 4GB
<span class="hc-k">$</span> deployctl apply --plan plan.json
<span class="hc-o">ok</span>  容器 healthy &middot; 仅绑定 127.0.0.1
<span class="hc-k">$</span> deployctl verify --target gateway-host
<span class="hc-o">ok</span>  TLS A &middot; HSTS &middot; 安全头 6/6 &middot; 日志已脱敏
<span class="hc-c"># 交接内容：运维手册 + 备份方案 + 完全属于你的密钥</span></code></pre>
</div>
</div>

<section class="case-proof">
<h2>先看交付方法，不靠宣传口号</h2>
<div class="proof-panel">
  <div><span class="proof-step">01</span><h3>检查</h3><p class="dim">修改前先核查主机、网络暴露面、密钥保管与回滚路径。</p></div>
  <div><span class="proof-step">02</span><h3>部署</h3><p class="dim">按书面配置落地，缩小公网暴露面，并使用可吊销的虚拟密钥。</p></div>
  <div><span class="proof-step">03</span><h3>验证</h3><p class="dim">实际探测 TLS、健康状态、故障转移、日志脱敏、备份和恢复，不把“容器在运行”当作交付证据。</p></div>
</div>
<p>可以先看<a href="case-study/">匿名化案例模式</a>，或直接检查<a href="docs/">公开版运维手册</a>。</p>
</section>

<h2>团队常见的三个问题</h2>
<div class="grid c3">
  <div class="card glass"><h3>密钥散落各处</h3><p class="dim">API 密钥被随手
  贴进笔记、CI 变量和各种桌面工具，没有人能说清一共发出去多少把、各自用在哪
  里，更没有人敢轮换。</p></div>
  <div class="card glass"><h3>成本一笔糊涂账</h3><p class="dim">账单月底才
  出，具体是哪个团队、哪个功能、哪个失控的脚本烧掉了预算，服务商控制台给不
  出答案。</p></div>
  <div class="card glass"><h3>代码被厂商绑死</h3><p class="dim">每个服务各自
  硬编码一家厂商的 SDK，想换模型、想在故障时切换备用线路，都要改代码、重新
  上线。</p></div>
</div>

<h2>网关层能带来什么</h2>
<p>自托管网关（LiteLLM、one-api、Sub2API 等开源项目）在所有上游服务商之前
统一提供一个 OpenAI 兼容接口。业务侧使用的是可随时创建、限额、吊销的
<em>虚拟密钥</em>，真正的服务商密钥集中存放、严格管控。用量按密钥计量，
速率限制、模型路由、故障转移一应俱全——而这一切都运行在你自己的服务器上。</p>

<h2>服务内容</h2>
<div class="grid c2">
  <div class="card"><h3>部署</h3><p class="dim">Docker Compose 或 systemd 方
  案，反向代理配齐 HTTPS 与 HSTS，容器以非 root 运行，目录结构有文档可查，
  升级路径经过实际演练。</p></div>
  <div class="card"><h3>加固</h3><p class="dim">密钥统一入库并收紧权限，管理
  面与数据面隔离，安全响应头、fail2ban、日志脱敏——任何情况下密钥都不会以明
  文出现在日志里。</p></div>
  <div class="card"><h3>运维</h3><p class="dim">健康检查与告警、用量看板、定
  期备份与恢复演练（附书面 runbook），以及按团队、按密钥的配额策略。</p></div>
  <div class="card"><h3>交接</h3><p class="dim">项目结束时，基础设施、文档与
  讲解录屏全部移交。系统的正常运转不依赖任何外部个人——这本身就是交付标准
  之一。</p></div>
</div>

<h2>服务边界</h2>
<div class="notice">本工作室部署的网关，只承载<strong>你自己的服务商账号与
API 密钥</strong>（或你的组织获得正式授权使用的密钥）产生的流量。以下业务
一概不做：将消费级订阅转售为 API、共享或拼池账号配额、绕过服务商速率限制、
提取账号凭证。完整清单见<a href="compliance/">合规页</a>。</div>

<section class="final-cta">
  <div><p class="kicker">先确认环境，再谈部署方案</p>
  <h2>需要一套交接后<wbr>仍能独立运维的网关？</h2>
  <p class="dim">邮件说明目标软件、服务器限制和需要接入的上游。我会先确认是否适合承接及工作范围，再开始部署。</p></div>
  <a class="btn contact-mail" href="mailto:hello@aigatewaylab.xyz?subject=Gateway%20deployment%20review">申请部署评估</a>
</section>
"""

ARCH_TITLE = "网关架构"
ARCH_DESC = "自托管 AI API 网关参考架构：信任边界、数据流、密钥保管与故障域设计。"
ARCH_BODY = """
<h1>架构</h1>
<p class="lead">下面是实际部署采用的参考架构。比组件本身更重要的，是信任边界
划在哪里。</p>

<h2>数据流</h2>
<div class="diagram">
 客户端（你的业务服务、内部工具）
   │  虚拟密钥 (vk-...)，永远不是服务商密钥
   ▼
┌───────────────────────────────────────────────┐
│  反向代理  (Caddy / nginx)                    │  TLS、HSTS、限流、
│  - 终结 HTTPS                                 │  安全响应头
└───────────────┬───────────────────────────────┘
                ▼
┌───────────────────────────────────────────────┐
│  网关  (LiteLLM / one-api 等)                 │
│  - 认证：虚拟密钥 → 团队、配额、模型          │
│  - 路由：模型名 → 上游池                      │
│  - 用量计量、请求日志（已脱敏）               │
│  - 故障转移：自动重试下一个健康上游           │
└──────┬──────────────────────────┬─────────────┘
       ▼                          ▼
┌──────────────┐          ┌──────────────┐
│ 密钥保管     │          │ SQLite/Postgres│
│ (env/文件,   │          │ 用量、密钥、   │
│  0600, 不可  │          │ 审计日志       │
│  经 web 访问)│          └──────────────┘
└──────┬───────┘
       ▼  服务商密钥 (sk-...，归你所有)
 上游服务商（OpenAI、Anthropic、Google 等官方 API）
</div>

<h2>信任边界</h2>
<table>
<tr><th>边界</th><th>规则</th></tr>
<tr><td>公网 → 代理</td><td>对外只开放 443。管理后台绝不暴露在公网，只能通过
SSH 隧道或 VPN 访问。</td></tr>
<tr><td>代理 → 网关</td><td>走回环或内网。网关容器任何时候都不绑定公网端
口。</td></tr>
<tr><td>网关 → 密钥库</td><td>服务商密钥仅网关进程用户可读（0600、非
root），不会出现在日志、报错信息或返回给客户端的任何内容里。</td></tr>
<tr><td>客户端 → 网关</td><td>客户端只持有带配额、可吊销的虚拟密钥。即便某个
客户端被攻破，损失也只是一把虚拟密钥的额度，动不到服务商账号。</td></tr>
</table>

<h2>故障域</h2>
<ul>
<li><strong>上游服务商故障：</strong>健康检查将其标记为不健康，路由器把请求
自动重试到同一档位的其他服务商。<a href="../case-study/">案例复盘</a>中有一
条结构真实的故障转移时间线（数据为合成）。</li>
<li><strong>网关进程崩溃：</strong>systemd/compose 自动重启，外部健康探针在
状态变化时各告警一次。</li>
<li><strong>主机整体丢失：</strong>数据库与配置每夜加密备份；恢复流程写成文
档并实际演练过。恢复耗时取决于镜像拉取与 DNS 生效速度，交接时按实际环境测
出，不做空头估算。</li>
</ul>
"""

DEMO_TITLE = "在线演示 — 模拟网关控制台"
DEMO_DESC = ("自托管 AI 网关的演示控制台：合成的上游、密钥、请求日志，"
             "并可回放一次故障转移。")
DEMO_BODY = """
<h1>演示控制台</h1>
<div class="notice"><strong>以下内容全部为合成数据。</strong>上游是模拟的，
账号与余额是虚构的，请求日志是程序生成的。本站未接入任何真实服务商账号。
状态每 15 分钟自动重置，所有写操作只影响浏览器本地的一次性副本。控制台内
文案保留英文，与生产环境的终端习惯保持一致。</div>

<div class="demo-toolbar">
  <span class="stat">demo state: <span id="d-age">fresh</span></span>
  <button class="btn ghost" id="d-reset" type="button">重置演示状态</button>
  <button class="btn ghost" id="d-replay" type="button">回放故障转移事件</button>
</div>

<h2>上游健康状态</h2>
<div id="d-upstreams" class="grid c3"></div>

<h2>虚拟密钥</h2>
<p class="dim">试着创建、吊销几把密钥，观察审计日志的联动变化。密钥仅在创建
时完整显示一次，此后只显示前缀——与生产环境执行同一套策略。</p>
<p><button class="btn" id="d-newkey" type="button">+ 创建虚拟密钥</button></p>
<div class="scroll-x"><table id="d-keys"></table></div>

<h2>请求日志（已脱敏，与生产一致）</h2>
<div class="scroll-x"><table id="d-log"></table></div>

<h2>审计日志</h2>
<div class="scroll-x"><table id="d-audit"></table></div>

<script src="../../static/js/demo.js" defer></script>
"""

DOCS_TITLE = "部署文档"
DOCS_DESC = ("自托管 AI API 网关的完整部署流程：Docker、HTTPS、备份、"
             "升级与监控，逐步展开。")
DOCS_BODY = """
<h1>部署文档</h1>
<p class="lead">这是交付给每位客户的 runbook 公开精简版。所有命令都在演示
所用的开源网关栈上实际验证过；主机名与路径为示例值。</p>

<h2>1 · Docker 部署</h2>
<pre><code># docker-compose.yml（节选——完整文件见 GitHub 仓库）
services:
  gateway:
    image: ghcr.io/berriai/litellm:main-stable   # 或你选定的网关
    user: "10001:10001"            # 非 root
    read_only: true                # 只读根文件系统
    tmpfs: [/tmp]
    env_file: /srv/gateway/secrets.env   # 0600, root:root
    expose: ["4000"]               # 仅内部——不绑定公网
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://127.0.0.1:4000/health/liveliness"]
      interval: 30s
      retries: 3</code></pre>
<p>基本原则：网关容器不直接发布宿主机端口，对外的永远只有反向代理。密钥放在
root 所有、权限 0600 的 env 文件中，以只读方式挂载。容器使用固定的非 root
UID，根文件系统只读。</p>

<h2>2 · HTTPS 与证书自动续期</h2>
<pre><code># Caddyfile —— 8 行配齐 HTTPS、HSTS 与安全头
example.com {{
  encode gzip
  header {{
    Strict-Transport-Security "max-age=31536000; includeSubDomains"
    X-Content-Type-Options nosniff
    X-Frame-Options DENY
    Referrer-Policy strict-origin-when-cross-origin
  }}
  reverse_proxy 127.0.0.1:4000
}}</code></pre>
<p>Caddy 自动签发并续期证书。如果选 nginx，则由 certbot 配合 systemd 定时器
完成同样的工作，两套方案仓库里都有现成配置。</p>

<h2>3 · 备份：能恢复的才算数</h2>
<pre><code># 每夜执行：导出数据库与配置，加密归档，保留 14 天
sqlite3 /srv/gateway/data/gateway.db ".backup /tmp/gw.db"
tar czf - -C /srv/gateway config data | age -r "$BACKUP_PUBKEY" \\
  &gt; /backup/gateway-$(date +%F).tar.gz.age
find /backup -name "gateway-*.age" -mtime +14 -delete</code></pre>
<p>从未做过恢复演练的备份，只是一份心理安慰。runbook 中固定了季度恢复演练：
恢复到临时目录，在内部端口拉起第二个网关实例，跑一轮冒烟测试，确认无误后
拆除。</p>

<h2>4 · 升级流程</h2>
<ol>
<li>先读 release notes，确认有没有数据库 schema 迁移。</li>
<li>做快照：按上述方式备份，并记录当前镜像 digest。</li>
<li>拉取新镜像、重启服务，紧盯健康端点和错误率。</li>
<li>回归验证：跑冒烟套件（创建密钥 → 发起一次对话请求 → 确认产生用量记
录）。</li>
<li>准备好回滚：上一个镜像 digest 加恢复后的数据库。因为演练过，回滚耗时是
每套环境实测出来的数字，不是估计。</li>
</ol>

<h2>5 · 监控</h2>
<ul>
<li><code>/health</code> 端点由外部探针巡检，按状态变化告警——故障一条、恢复
一条，不刷屏。</li>
<li>主机层面持续检查磁盘、内存与证书有效期。</li>
<li>用量异常必须查明归属：某把虚拟密钥的流量突增，应当能定位到一次具体调
用，而不是不了了之。</li>
</ul>
"""

SEC_TITLE = "安全模型"
SEC_DESC = "自托管 AI API 网关的密钥保管、最小权限、日志脱敏与事故处置方案。"
SEC_BODY = """
<h1>安全</h1>
<p class="lead">网关运维中真正见功力的部分，往往在演示顺利时看不见，在事故
发生时起决定作用。</p>

<h2>密钥保管</h2>
<table>
<tr><th>秘密</th><th>存放位置</th><th>绝不允许出现的位置</th></tr>
<tr><td>服务商密钥 (sk-…)</td><td>宿主机上权限 0600 的 env 文件，或密钥管理
服务；仅网关进程用户可读</td><td>日志、报错正文、客户端响应、git、容器镜
像、明文备份</td></tr>
<tr><td>虚拟密钥 (vk-…)</td><td>网关数据库中散列存储</td>
<td>创建之后的任何完整展示——界面只显示一次，日志只记前缀</td></tr>
<tr><td>管理员凭证</td><td>密码管理器，并开启 TOTP</td>
<td>群聊消息、仓库里的 .env 文件</td></tr>
</table>

<h2>最小权限</h2>
<ul>
<li>容器以专用非 root UID 运行，根文件系统只读，临时文件走 tmpfs。</li>
<li>管理面只绑定 localhost，访问必须经 SSH 隧道或 VPN。公网接口只承载推理
流量。</li>
<li>数据库账号在运行期不持有 DDL 权限，迁移作为独立步骤单独执行。</li>
<li>每个客户团队使用独立的虚拟密钥，各自带模型白名单与预算上限——吊销任何
一个客户，都不会波及其他客户。</li>
</ul>

<h2>日志脱敏</h2>
<p>网关处在请求链路的正中间，它的日志天然就是高价值目标。部署时默认做以下
脱敏处理：</p>
<ul>
<li><code>Authorization</code> 头 → <code>vk-****后4位</code></li>
<li>提示词与补全正文 → 默认只记录 token 数；仅当客户为排障显式开启内容日志
时才记录，且设定自动过期。</li>
<li>上游报错正文 → 服务商密钥在错误信息到达客户端或日志之前即被剥离。</li>
</ul>
<p><a href="../demo/">演示</a>中的请求日志展示的正是这套形态：满足运维需
要，但没有窃取价值。</p>

<h2>事故处置（演练过的流程，不是纸面预案）</h2>
<table>
<tr><th>事故</th><th>处置</th></tr>
<tr><td>虚拟密钥泄露</td><td>立即吊销（请求直接失败关闭），复查其活跃窗口内
的审计日志，按原有策略补发新钥。影响范围：仅这把密钥的配额。</td></tr>
<tr><td>疑似服务商密钥泄露</td><td>在服务商侧轮换，更新密钥库，重启网关（重
试代理可以吃掉这几秒钟的中断），最后用金丝雀请求确认恢复。</td></tr>
<tr><td>疑似主机沦陷</td><td>第一时间在服务商侧吊销服务商密钥——那才是真正值
钱的东西。之后用干净镜像加加密备份重建，绝不从可疑主机上恢复任何可执行文
件。</td></tr>
<tr><td>数据丢失</td><td>恢复前一夜的加密备份；备份点之后的用量记录确认丢失
就如实说明，账务以服务商控制台为准进行对账。</td></tr>
</table>
"""

CASE_TITLE = "案例复盘：密钥收拢、模型路由与一次上游故障"
CASE_DESC = ("一次匿名化的网关交付复盘：收拢散落的 API 密钥、建立模型路由，"
             "并平稳扛过一次上游服务商故障。")
CASE_BODY = """
<h1>案例复盘</h1>
<div class="notice">本案例由真实的自托管网关交付经历匿名化、泛化而来。身份
信息、主机名、具体数字与厂商组合均已调整；值得借鉴的是时间线结构与故障处理
模式。文中数字仅用于说明，不是账单记录。</div>

<h2>交付前的状况</h2>
<p>一个小型产品团队，三个服务对接两家 AI 服务商。每个服务各自在 env 文件里
存了一把服务商密钥，其中一把曾在一次事故排查中被贴进聊天工具转发过，此后
再没轮换。用量没有按团队的视图，账单只有一个总数。</p>

<h2>第一阶段 · 收拢密钥（第 1 周）</h2>
<ul>
<li>在内部子域名上部署网关（Docker Compose、非 root、只读根文件系统），前置
Caddy，配齐 HTTPS 与 HSTS。</li>
<li>两把服务商密钥全部收入密钥库；每个服务改发一把虚拟密钥，附带月度预算与
模型白名单。</li>
<li>各服务只需修改 <code>base_url</code> 和密钥就完成了切换——网关说的是同
一种 API 方言，业务代码一行不动。</li>
<li>切换完成<em>之后</em>，再轮换那把在聊天工具里泄露过的密钥。客户端零改
动——这正是加一层网关的意义所在。</li>
</ul>

<h2>第二阶段 · 路由策略（第 2 周）</h2>
<ul>
<li>内部工具走低价快速的模型档位，面向客户的功能走高级档位——用密钥策略强制
执行，不靠开发者自觉。</li>
<li>依据两周实测流量，为每把密钥设定速率上限。</li>
<li>启用每夜加密备份；外部健康探针按状态变化告警。</li>
</ul>

<h2>第三阶段 · 一次真正检验价值的故障</h2>
<p>上线数周后，主力服务商出现区域性故障，错误率与延迟同时飙升（这类模式在
任何一家大型服务商的 status page 历史里都能找到）。以下是网关视角的时间
线，<a href="../demo/">演示</a>中用合成数据复现了同一过程：</p>
<div class="diagram">
T+0m   上游 A 错误率超过阈值；健康检查将 A 标记为 degraded
T+0m   路由器开始把失败请求重试到同档位的上游 B
T+2m   探针告警一次："upstream-a: FAIL"——只此一条，不刷屏
T+31m  服务商恢复；健康检查连续两次通过；A 重新进入轮转
T+31m  探针告警一次："upstream-a: RECOVERED"
客户可感知的影响：约 2 分钟的 p95 延迟升高；没有出现 5xx 峰值
</div>

<h2>为什么这次故障如此平淡（这正是设计目标）</h2>
<ul>
<li>故障转移在交接时做过<em>强制断流演练</em>——真实事故发生时，它已经是第
二次运行。</li>
<li>告警做了去重，最终只有两条消息，而不是两百条。</li>
<li>复盘报告只写了一段话，因为完整时间线本来就在审计日志里。</li>
</ul>

<h2>交接</h2>
<p>团队最终拿到 runbook、恢复演练录屏和全部管理员权限。外部参与到此为止；
系统此后独立运转，不依赖任何个人——这正是本次交付的验收标准。</p>
"""

COMP_TITLE = "合规与业务边界"
COMP_DESC = ("本工作室承接什么、拒绝什么：自托管 AI 网关部署的分服务商合规"
             "对照表。")
COMP_BODY = """
<h1>合规</h1>
<p class="lead">网关技术是把双刃剑：同样一套路由能力，既可以帮企业管好自有
密钥，也可能被拿去转售消费级订阅。本页把界线白纸黑字写清楚。</p>

<h2>承接的业务</h2>
<ul>
<li>部署与运维只路由<strong>贵组织自有 API 密钥</strong>（BYOK，来自服务商
官方 API 计划）流量的网关。</li>
<li>在<em>你自己</em>的账号范围内提供虚拟密钥管理、配额、用量计量、路由与
故障转移。</li>
<li>安全加固、监控、备份与完整交接。</li>
</ul>

<h2>无论出价多少都不做的业务</h2>
<ul>
<li>把消费级订阅（ChatGPT Plus、Claude Pro/Max、Gemini 消费版等）改造成可
转售的 API 接入。</li>
<li>账号拼池、配额共享、账号容量转售。</li>
<li>绕过服务商的速率限制、并发上限或反滥用机制。</li>
<li>提取、买卖或转移账号凭证。</li>
<li>通过抓取私有 Web 界面来伪造 API 访问。</li>
</ul>

<h2>服务商对照表（API 接入方式）</h2>
<div class="notice">以下摘要基于 2026-07-26 查阅的各服务商条款。条款随时可能
调整，引用前请以官方原文为准。本表是工程合规摘要，不构成法律意见。</div>
<table>
<tr><th>服务商</th><th>官方 API（BYOK）</th><th>经网关中继消费级订阅</th>
<th>备注</th></tr>
<tr><td>OpenAI</td><td class="ok-cell">允许——平台 API 密钥</td>
<td>不允许用于第三方转售中继</td><td>平台条款将 API 用量绑定到账号持有者；
消费级 ChatGPT 条款仅覆盖个人、非程序化使用。</td></tr>
<tr><td>Anthropic</td><td class="ok-cell">允许——控制台签发的 API 密钥</td>
<td>不允许用于第三方转售中继</td><td>商业条款明确区分 API 服务与消费级
Claude 应用。</td></tr>
<tr><td>Google (Gemini)</td><td class="ok-cell">允许——AI Studio / Vertex
密钥</td><td>不允许用于第三方转售中继</td>
<td>消费级套餐与 Cloud API 是条款相互独立的两种产品。</td></tr>
<tr><td>开放权重托管（Together、Fireworks、自托管 vLLM…）</td>
<td class="ok-cell">允许——标准 API 密钥或自有硬件</td>
<td>n/a</td><td>对成本敏感的分层路由而言，这是最干净的一条路。</td></tr>
</table>
<p class="dim">凡不在服务商官方计划覆盖范围内的接入方式，本站一律按「未验
证」处理：不演示、不教学、也不会出现在 demo 里。</p>

<h2>关于本站</h2>
<ul>
<li><a href="../demo/">演示</a>只连接<strong>模拟上游</strong>：账号、余额、
日志全部是假的。这台服务器上没有接入任何真实服务商账号。</li>
<li>本站是独立的部署能力演示，与 Sub2API 项目及任何上游 AI 服务商均无隶属、
背书或合作关系。提及服务商名称仅为说明互操作性，未使用任何品牌 Logo。</li>
<li>部署过程遵守所用开源网关软件的许可证——包括 LGPL-3.0-or-later 组件的源码
可得性与修改声明义务。每次交付均附许可证文本。</li>
</ul>
"""
