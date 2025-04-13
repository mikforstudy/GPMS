<script>
    import { onMount } from "svelte";
    import axios from "axios";
    import '$lib/style.css';

    let username = "";
    let student_id = 0;
    let loading = false;
    let error = null;
    let success = false;
    let fileList = [];
    let fileCount = 0;

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            student_id = localStorage.getItem("student_id");
            getFileList();
        }
    });

    // 获取文件列表预览
    async function getFileList() {
        try {
            // 更新API路径为正确的路径
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/file/list/${student_id}`);
            fileList = response.data || [];
            fileCount = fileList.length;
        } catch (err) {
            console.error("获取文件列表失败", err);
            // 不显示错误，因为这只是辅助功能
        }
    }

    // 导出所有文件
    async function exportAllFiles() {
        loading = true;
        error = null;
        success = false;
        
        try {
            // 更新为正确的API路径
            const downloadUrl = `http://127.0.0.1:8000/api/v1/file/student/${student_id}`;
            
            // 创建一个隐藏的a标签来触发下载
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', `student_${student_id}_files.zip`);
            document.body.appendChild(link);
            link.click();
            
            // 清理DOM
            document.body.removeChild(link);
            
            success = true;
        } catch (err) {
            console.error("导出文件失败", err);
            error = err.response?.data?.detail || "导出文件失败，请稍后重试";
        } finally {
            loading = false;
        }
    }
</script>

<div class="max-h-screen bg-base-200 p-4">
    <div class="container mx-auto px-4 py-8">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-bold">文件导出</h1>
            <div class="text-right">
                <p class="text-lg">{username}</p>
                <p class="text-sm opacity-75">学号：{student_id}</p>
            </div>
        </div>

        <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
                <h2 class="card-title">导出所有文件</h2>
                <p class="py-4">
                    点击下方按钮将导出您的所有文件为压缩包格式。导出过程可能需要一些时间，请耐心等待。
                    {#if fileCount > 0}
                        <br>系统检测到您有约 <span class="font-bold text-primary">{fileCount}</span> 个文件。
                    {/if}
                </p>

                {#if error}
                    <div class="alert alert-error mt-4">
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>{error}</span>
                    </div>
                {/if}

                {#if success}
                    <div class="alert alert-success mt-4">
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>导出成功！文件正在下载中...</span>
                    </div>
                {/if}

                <div class="card-actions justify-end mt-6">
                    <button 
                        class="btn btn-primary {loading ? 'loading' : ''}" 
                        on:click={exportAllFiles}
                        disabled={loading}
                    >
                        {#if loading}
                            <span class="loading loading-spinner"></span>
                            导出中...
                        {:else}
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                            </svg>
                            导出所有文件
                        {/if}
                    </button>
                </div>
            </div>
        </div>

        {#if fileList.length > 0}
            <div class="card bg-base-100 shadow-xl mt-8">
                <div class="card-body">
                    <h2 class="card-title">文件列表预览</h2>
                    <div class="overflow-x-auto">
                        <table class="table table-zebra">
                            <thead>
                                <tr>
                                    <th>文件名</th>
                                    <th>修改日期</th>
                                    <th>大小</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each fileList as file}
                                    <tr>
                                        <td>{file.name}</td>
                                        <td>{file.modified_date}</td>
                                        <td>{file.size}</td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        {/if}

        <div class="card bg-base-100 shadow-xl mt-8">
            <div class="card-body">
                <h2 class="card-title">说明</h2>
                <div class="py-2">
                    <ul class="list-disc list-inside space-y-2">
                        <li>所有文件将被压缩为一个ZIP格式的压缩包</li>
                        <li>导出操作可能需要一些时间，取决于文件数量和大小</li>
                        <li>如果您的文件较多，请耐心等待下载完成</li>
                        <li>如果遇到问题，请刷新页面重试或联系系统管理员</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>