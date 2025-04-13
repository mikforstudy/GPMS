<script>
    import { onMount } from "svelte";
    import axios from "axios";

    // 教师用户名
    let username = "";
    let defenses = []; // 存储答辩信息列表
    let loading = true;
    let error = null;
    
    // 按答辩阶段分类的数据
    let proposalDefenses = [];
    let midtermDefenses = [];
    let finalDefenses = [];
    
    // 激活的标签页
    let activeTab = "proposal"; // 默认显示开题答辩

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            fetchDefenseInfo();
        }
    });

    // 获取该教师名下所有答辩信息
    async function fetchDefenseInfo() {
        try {
            loading = true;
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/defense/teacher/${username}`);
            defenses = response.data;
            console.log("获取的答辩信息:", defenses);
            
            // 按照答辩阶段分组
            proposalDefenses = defenses.filter(defense => defense.defense_phase.includes("开题"));
            midtermDefenses = defenses.filter(defense => defense.defense_phase.includes("中期") || defense.defense_phase.includes("中题"));
            finalDefenses = defenses.filter(defense => defense.defense_phase.includes("最终"));
            
        } catch (err) {
            error = `获取答辩信息失败: ${err.message}`;
            console.error("获取答辩信息失败:", err);
        } finally {
            loading = false;
        }
    }
    
    // 切换标签页
    function setActiveTab(tab) {
        activeTab = tab;
    }
    
    // 格式化日期显示
    function formatDate(dateString) {
        if (!dateString) return '未知时间';
        
        // 简单处理日期格式
        if (dateString.includes('T')) {
            return dateString.split('T')[0];
        }
        return dateString;
    }
    
    // 获取状态标签样式
    function getStatusBadgeClass(status) {
        switch (status) {
            case '已完成': return 'badge-success';
            case '进行中': return 'badge-warning';
            case '未开始': return 'badge-info';
            default: return 'badge-ghost';
        }
    }
</script>

<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">答辩信息管理</h1>
    
    <!-- 错误提示 -->
    {#if error}
        <div class="alert alert-error shadow-lg mb-6">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>{error}</span>
            </div>
        </div>
    {/if}
    
    <!-- 加载指示器 -->
    {#if loading}
        <div class="flex justify-center items-center h-64">
            <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>
    <!-- 无数据提示 -->
    {:else if defenses.length === 0}
        <div class="alert alert-info shadow-lg">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>暂无答辩安排信息。</span>
            </div>
        </div>
    <!-- 答辩信息展示 -->
    {:else}
        <!-- 标签页 -->
        <div class="tabs tabs-boxed mb-4">
            <a class="tab {activeTab === 'proposal' ? 'tab-active' : ''}" on:click={() => setActiveTab('proposal')}>开题答辩</a>
            <a class="tab {activeTab === 'midterm' ? 'tab-active' : ''}" on:click={() => setActiveTab('midterm')}>中期答辩</a>
            <a class="tab {activeTab === 'final' ? 'tab-active' : ''}" on:click={() => setActiveTab('final')}>最终答辩</a>
        </div>
        
        <!-- 开题答辩表格 -->
        <div class={activeTab === 'proposal' ? 'block' : 'hidden'}>
            <h2 class="text-xl font-semibold mb-3">开题答辩安排</h2>
            {#if proposalDefenses.length === 0}
                <div class="alert alert-info">暂无开题答辩安排</div>
            {:else}
                <div class="overflow-x-auto">
                    <table class="table w-full">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>学生姓名</th>
                                <th>学号</th>
                                <th>论文题目</th>
                                <th>答辩日期</th>
                                <th>答辩教室</th>
                                <th>答辩小组</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each proposalDefenses as defense, index}
                                <tr class="hover">
                                    <td>{index + 1}</td>
                                    <td>{defense.student_name}</td>
                                    <td>{defense.student_id}</td>
                                    <td class="max-w-xs truncate" title={defense.project_title}>{defense.project_title}</td>
                                    <td>{formatDate(defense.defense_date)}</td>
                                    <td>{defense.defense_class}</td>
                                    <td>{defense.defense_group}</td>
                                    <td>
                                        <span class="badge {getStatusBadgeClass(defense.status)}">{defense.status}</span>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>
        
        <!-- 中期答辩表格 -->
        <div class={activeTab === 'midterm' ? 'block' : 'hidden'}>
            <h2 class="text-xl font-semibold mb-3">中期答辩安排</h2>
            {#if midtermDefenses.length === 0}
                <div class="alert alert-info">暂无中期答辩安排</div>
            {:else}
                <div class="overflow-x-auto">
                    <table class="table w-full">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>学生姓名</th>
                                <th>学号</th>
                                <th>论文题目</th>
                                <th>答辩日期</th>
                                <th>答辩教室</th>
                                <th>答辩小组</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each midtermDefenses as defense, index}
                                <tr class="hover">
                                    <td>{index + 1}</td>
                                    <td>{defense.student_name}</td>
                                    <td>{defense.student_id}</td>
                                    <td class="max-w-xs truncate" title={defense.project_title}>{defense.project_title}</td>
                                    <td>{formatDate(defense.defense_date)}</td>
                                    <td>{defense.defense_class}</td>
                                    <td>{defense.defense_group}</td>
                                    <td>
                                        <span class="badge {getStatusBadgeClass(defense.status)}">{defense.status}</span>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>
        
        <!-- 最终答辩表格 -->
        <div class={activeTab === 'final' ? 'block' : 'hidden'}>
            <h2 class="text-xl font-semibold mb-3">最终答辩安排</h2>
            {#if finalDefenses.length === 0}
                <div class="alert alert-info">暂无最终答辩安排</div>
            {:else}
                <div class="overflow-x-auto">
                    <table class="table w-full">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>学生姓名</th>
                                <th>学号</th>
                                <th>论文题目</th>
                                <th>答辩日期</th>
                                <th>答辩教室</th>
                                <th>答辩小组</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each finalDefenses as defense, index}
                                <tr class="hover">
                                    <td>{index + 1}</td>
                                    <td>{defense.student_name}</td>
                                    <td>{defense.student_id}</td>
                                    <td class="max-w-xs truncate" title={defense.project_title}>{defense.project_title}</td>
                                    <td>{formatDate(defense.defense_date)}</td>
                                    <td>{defense.defense_class}</td>
                                    <td>{defense.defense_group}</td>
                                    <td>
                                        <span class="badge {getStatusBadgeClass(defense.status)}">{defense.status}</span>
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            {/if}
        </div>
    {/if}
</div>