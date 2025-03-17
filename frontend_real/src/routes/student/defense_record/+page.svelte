<script>
    import { onMount } from "svelte";
    import axios from "axios";
    import { tick } from 'svelte';

    let username = "";
    let student_id = 0;
    let defenses = [];
    let loading = false;
    let errorMessage = "";
    let successMessage = "";

    // 可选的答辩状态
    const statusOptions = ["已完成", "未参与"];

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            student_id = localStorage.getItem("student_id");
            fetchDefenseData();
        }
    });

    async function fetchDefenseData() {
        try {
            loading = true;
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/defense/student/${student_id}`);
            defenses = response.data;
            loading = false;
        } catch (error) {
            console.error("Error fetching defense data:", error);
            errorMessage = "获取答辩数据失败";
            loading = false;
        }
    }

    async function updateDefenseStatus(defense, newStatus) {
        try {
            loading = true;
            errorMessage = "";
            successMessage = "";
            
            const response = await axios.put(
                `http://127.0.0.1:8000/api/v1/defense/${student_id}/${defense.defense_phase}`, 
                { status: newStatus }
            );
            
            // 更新本地数据
            await fetchDefenseData();
            
            successMessage = "答辩状态已更新";
            loading = false;
            
            // 3秒后清除成功消息
            setTimeout(() => {
                successMessage = "";
                tick();
            }, 3000);
            
        } catch (error) {
            console.error("Error updating defense status:", error);
            errorMessage = error.response?.data?.detail || "更新答辩状态失败";
            loading = false;
        }
    }
</script>

<h1 class="text-2xl font-bold mb-4">答辩状态管理</h1>

{#if errorMessage}
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
        <span class="block sm:inline">{errorMessage}</span>
    </div>
{/if}

{#if successMessage}
    <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4" role="alert">
        <span class="block sm:inline">{successMessage}</span>
    </div>
{/if}

{#if loading}
    <div class="flex justify-center items-center my-8">
        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
    </div>
{:else}
    <div class="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-md">
        <table class="min-w-full divide-y divide-gray-200">
            <!-- head -->
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">#</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">学生姓名</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">教师姓名</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">项目标题</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">答辩教室</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">答辩组</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">答辩阶段</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">答辩日期</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">当前状态</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                {#each defenses as defense, index}
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{index + 1}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.student_name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.teacher_name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.project_title}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.defense_class}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.defense_group}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.defense_phase}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{defense.defense_date}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm">
                        <span class={defense.status === '已取消' 
                            ? 'text-red-600 font-medium' 
                            : defense.status === '已完成' 
                                ? 'text-green-600 font-medium'
                                : defense.status === '已确认'
                                    ? 'text-blue-600 font-medium'
                                    : 'text-yellow-600 font-medium'
                        }>
                            {defense.status}
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        <div class="flex items-center space-x-2">
                            <select 
                                class="border border-gray-300 rounded px-2 py-1 text-sm"
                                on:change={(e) => updateDefenseStatus(defense, e.target.value)}
                            >
                                <option value="" disabled selected>修改状态</option>
                                {#each statusOptions as status}
                                    {#if status !== defense.status}
                                        <option value={status}>{status}</option>
                                    {/if}
                                {/each}
                            </select>
                        </div>
                    </td>
                </tr>
                {/each}
                
                {#if defenses.length === 0}
                <tr>
                    <td colspan="10" class="px-6 py-4 text-center text-sm text-gray-500">暂无答辩记录</td>
                </tr>
                {/if}
            </tbody>
        </table>
    </div>
{/if}