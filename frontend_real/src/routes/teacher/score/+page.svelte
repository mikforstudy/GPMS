<script>
    import { onMount } from "svelte";
    import axios from "axios";

    // 教师用户名
    let username = "";
    let scores = []; // 存储评分信息列表
    let loading = true;
    let error = null;
    let successMessage = "";
    
    // 编辑相关变量
    let showEditModal = false;
    let currentScore = null;
    let newScoreValue = "";
    let submitting = false;

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            fetchScores();
        }
    });

    // 获取该教师名下所有学生的评分信息
    async function fetchScores() {
        try {
            loading = true;
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/score/teacher/${username}`);
            scores = response.data;
            console.log("获取的评分信息:", scores);
        } catch (err) {
            error = `获取评分信息失败: ${err.message}`;
            console.error("获取评分信息失败:", err);
        } finally {
            loading = false;
        }
    }

    // 打开编辑模态框
    function openEditModal(score) {
        currentScore = {...score};
        newScoreValue = score.score === "待评定" ? "" : score.score;
        showEditModal = true;
    }

    // 关闭编辑模态框
    function closeEditModal() {
        showEditModal = false;
        currentScore = null;
        newScoreValue = "";
        submitting = false;
    }

    // 提交成绩修改
    async function submitScoreUpdate() {
        if (!currentScore || submitting) return;
        
        try {
            submitting = true;
            
            // 检查分数有效性
            if (!newScoreValue.trim()) {
                newScoreValue = "待评定";
            } else if (isNaN(newScoreValue) && !["优秀", "良好", "中等", "及格", "不及格", "待评定"].includes(newScoreValue)) {
                error = "请输入有效的分数或评级";
                submitting = false;
                return;
            }
            
            const response = await axios.put(`http://127.0.0.1:8000/api/v1/score/${currentScore.student_id}`, {
                score: newScoreValue
            });
            
            console.log("成绩更新成功:", response.data);
            
            // 更新本地列表
            const index = scores.findIndex(s => s.student_id === currentScore.student_id);
            if (index !== -1) {
                scores[index].score = newScoreValue;
                scores[index].update_time = new Date().toISOString();
            }
            
            // 显示成功消息
            successMessage = `已成功更新 ${currentScore.student_name} 的成绩为 ${newScoreValue}`;
            setTimeout(() => {
                successMessage = "";
            }, 3000);
            
            // 关闭模态框
            closeEditModal();
        } catch (err) {
            error = `更新成绩失败: ${err.message}`;
            console.error("更新成绩失败:", err);
        } finally {
            submitting = false;
        }
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
    
    // 获取成绩样式
    function getScoreBadgeClass(score) {
        if (score === "待评定") return "badge-ghost";
        if (score === "优秀" || parseInt(score) >= 90) return "badge-success";
        if (score === "良好" || parseInt(score) >= 80) return "badge-info";
        if (score === "中等" || parseInt(score) >= 70) return "badge-primary";
        if (score === "及格" || parseInt(score) >= 60) return "badge-warning";
        return "badge-error"; // 不及格
    }
</script>

<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">学生成绩评定</h1>
    
    <!-- 错误提示 -->
    {#if error}
        <div class="alert alert-error shadow-lg mb-6">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>{error}</span>
            </div>
        </div>
    {/if}
    
    <!-- 成功提示 -->
    {#if successMessage}
        <div class="alert alert-success shadow-lg mb-6">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>{successMessage}</span>
            </div>
        </div>
    {/if}
    
    <!-- 加载指示器 -->
    {#if loading}
        <div class="flex justify-center items-center h-64">
            <span class="loading loading-spinner loading-lg text-primary"></span>
        </div>
    <!-- 无数据提示 -->
    {:else if scores.length === 0}
        <div class="alert alert-info shadow-lg">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>暂无学生成绩信息。</span>
            </div>
        </div>
    <!-- 成绩信息表格 -->
    {:else}
        <div class="overflow-x-auto">
            <table class="table w-full">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>学生姓名</th>
                        <th>学号</th>
                        <th>毕业设计题目</th>
                        <th>成绩</th>
                        <th>最后更新时间</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {#each scores as score, index}
                        <tr class="hover">
                            <td>{index + 1}</td>
                            <td>{score.student_name}</td>
                            <td>{score.student_id}</td>
                            <td class="max-w-xs truncate" title={score.project_title}>{score.project_title}</td>
                            <td>
                                <span class="badge {getScoreBadgeClass(score.score)}">{score.score}</span>
                            </td>
                            <td>{formatDate(score.update_time)}</td>
                            <td>
                                <button 
                                    class="btn btn-primary btn-sm"
                                    on:click={() => openEditModal(score)}
                                >
                                    评定成绩
                                </button>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
    
    <!-- 编辑成绩模态框 -->
    {#if showEditModal && currentScore}
        <div class="fixed top-1/4 left-1/2 transform -translate-x-1/2 z-50">
            <div class="bg-white rounded-lg shadow-2xl w-full max-w-md">
                <!-- 模态框头部 -->
                <div class="p-4 border-b flex justify-between items-center">
                    <h2 class="text-xl font-semibold">评定学生成绩</h2>
                    <button class="btn btn-sm btn-circle" on:click={closeEditModal}>✕</button>
                </div>
                
                <div class="p-6 space-y-4">
                    <!-- 学生信息 -->
                    <div class="space-y-2">
                        <p><span class="font-semibold">学生姓名:</span> {currentScore.student_name}</p>
                        <p><span class="font-semibold">学号:</span> {currentScore.student_id}</p>
                        <p><span class="font-semibold">论文题目:</span> {currentScore.project_title}</p>
                        <p><span class="font-semibold">当前成绩:</span> {currentScore.score}</p>
                    </div>
                    
                    <!-- 成绩输入 -->
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text font-medium">输入评定成绩</span>
                        </label>
                        <div class="flex flex-col gap-2">
                            <input 
                                type="text" 
                                class="input input-bordered w-full" 
                                placeholder="请输入数字分数或选择等级" 
                                bind:value={newScoreValue}
                            />
                            <div class="text-xs text-gray-500">
                                可以输入分数(如85)或等级(优秀/良好/中等/及格/不及格)
                            </div>
                            <div class="flex flex-wrap gap-2 mt-2">
                                <button class="btn btn-xs" on:click={() => newScoreValue = "优秀"}>优秀</button>
                                <button class="btn btn-xs" on:click={() => newScoreValue = "良好"}>良好</button>
                                <button class="btn btn-xs" on:click={() => newScoreValue = "中等"}>中等</button>
                                <button class="btn btn-xs" on:click={() => newScoreValue = "及格"}>及格</button>
                                <button class="btn btn-xs" on:click={() => newScoreValue = "不及格"}>不及格</button>
                                <button class="btn btn-xs" on:click={() => newScoreValue = "待评定"}>待评定</button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 模态框底部 -->
                <div class="p-4 border-t flex justify-end space-x-2">
                    <button class="btn btn-ghost" on:click={closeEditModal}>取消</button>
                    <button 
                        class="btn btn-primary {submitting ? 'loading' : ''}" 
                        on:click={submitScoreUpdate}
                        disabled={submitting}
                    >
                        提交成绩
                    </button>
                </div>
            </div>
        </div>
    {/if}
</div>