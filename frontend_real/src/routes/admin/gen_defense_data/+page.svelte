<script>
    import axios from 'axios';
    import { onMount } from 'svelte';

    // 状态变量
    let isLoading = false;
    let result = null;
    let error = null;
    let notification = '';
    let notificationType = '';

    // 生成答辩数据
    async function generateDefenseData() {
        try {
            isLoading = true;
            notification = '正在生成答辩安排，请稍候...';
            notificationType = 'alert-info';
            error = null;
            
            // 调用后端 API 生成答辩数据
            const response = await axios.get('http://127.0.0.1:8000/api/v1/data-gen/generate-defense-data');
            
            result = response.data;
            notification = response.data.message;
            notificationType = response.data.status === 'success' ? 'alert-success' : 'alert-warning';
        } catch (err) {
            console.error('生成答辩安排失败:', err);
            error = err.response?.data?.detail || err.message || '未知错误';
            notification = `操作失败: ${error}`;
            notificationType = 'alert-error';
            result = null;
        } finally {
            isLoading = false;
        }
    }

    // 页面加载时可以执行的初始化操作
    onMount(() => {
        // 如果需要进行页面加载时的初始化，可以在这里添加代码
    });
</script>

<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">答辩数据生成工具</h1>

    <!-- 说明卡片 -->
    <div class="card bg-base-100 shadow-xl mb-6">
        <div class="card-body">
            <h2 class="card-title">功能说明</h2>
            <p>本工具用于自动生成答辩数据，将为项目表中的每个学生创建三种类型的答辩安排：（学生申报题目通过教师审核后可执行）</p>
            <p>正式情况下考虑使用解析excel的形式导入数据</p>
            <ul class="list-disc ml-6 mt-2">
                <li>开题答辩</li>
                <li>中期答辩</li>
                <li>最终答辩</li>
            </ul>
            <p class="mt-2">注意：已有完整答辩安排的学生将被自动跳过。</p>
        </div>
    </div>

    <!-- 操作区域 -->
    <div class="card bg-base-100 shadow-xl mb-6">
        <div class="card-body">
            <h2 class="card-title">操作面板</h2>
            <p>点击下方按钮开始生成答辩安排：</p>
            <div class="card-actions justify-end mt-4">
                <button 
                    class="btn btn-primary" 
                    on:click={generateDefenseData} 
                    disabled={isLoading}
                >
                    {#if isLoading}
                        <span class="loading loading-spinner"></span>
                        处理中...
                    {:else}
                        生成答辩安排
                    {/if}
                </button>
            </div>
        </div>
    </div>

    <!-- 通知区域 -->
    {#if notification}
        <div class="alert {notificationType} mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{notification}</span>
        </div>
    {/if}

    <!-- 结果展示区域 -->
    {#if result}
        <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
                <h2 class="card-title">操作结果</h2>
                <div class="overflow-x-auto">
                    <table class="table table-zebra w-full">
                        <tbody>
                            <tr>
                                <td class="font-semibold">总项目数</td>
                                <td>{result.detail.total_projects}</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">已处理学生</td>
                                <td>{result.detail.processed_students}</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">已跳过学生</td>
                                <td>{result.detail.skipped_students}</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">创建的记录数</td>
                                <td>{result.detail.created_records}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    {/if}
</div>