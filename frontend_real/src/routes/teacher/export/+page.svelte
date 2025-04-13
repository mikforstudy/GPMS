<script>
    import { onMount } from "svelte";
    import axios from "axios";
    import '$lib/style.css';

    let username = "";
    let students = [];
    let selectedStudentId = null;
    let loading = false;
    let error = null;
    let success = false;

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "教师";
            getStudentProjects();
        }
    });

    // 获取教师管理的学生项目列表
    async function getStudentProjects() {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/projects/teacher/${username}`);
            students = response.data || [];
        } catch (err) {
            console.error("获取学生项目列表失败", err);
            error = "无法加载学生项目列表，请稍后重试。";
        }
    }

    // 导出某个学生的所有文件
    async function exportStudentFiles() {
        if (!selectedStudentId) {
            error = "请选择一个学生进行导出。";
            return;
        }

        loading = true;
        error = null;
        success = false;

        try {
            const downloadUrl = `http://127.0.0.1:8000/api/v1/file/teacher/${selectedStudentId}`;
            
            // 创建一个隐藏的 a 标签来触发下载
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', `teacher_${selectedStudentId}_files.zip`);
            document.body.appendChild(link);
            link.click();
            
            // 清理 DOM
            document.body.removeChild(link);
            
            success = true;
        } catch (err) {
            console.error("导出文件失败", err);
            error = err.response?.data?.detail || "导出文件失败，请稍后重试。";
        } finally {
            loading = false;
        }
    }
</script>

<div class="max-h-screen bg-base-200 p-4">
    <div class="container mx-auto px-4 py-8">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-bold">教师文件导出</h1>
            <div class="text-right">
                
            </div>
        </div>

        <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
                <h2 class="card-title">选择学生并导出文件</h2>
                <p class="py-4">
                    请选择一个学生以导出其所有文件为压缩包格式。
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

                <div class="form-control mt-6">
                    <label class="label">
                        <span class="label-text">选择学生</span>
                    </label>
                    <select 
                        class="select select-bordered w-full"
                        bind:value={selectedStudentId}
                    >
                        <option value="" disabled selected>请选择一个学生</option>
                        {#each students as student}
                            <option value={student.id}>{student.student_name}（ID: {student.id}）</option>
                        {/each}
                    </select>
                </div>

                <div class="card-actions justify-end mt-6">
                    <button 
                        class="btn btn-primary {loading ? 'loading' : ''}" 
                        on:click={exportStudentFiles}
                        disabled={loading || !selectedStudentId}
                    >
                        {#if loading}
                            <span class="loading loading-spinner"></span>
                            导出中...
                        {:else}
                            导出文件
                        {/if}
                    </button>
                </div>
            </div>
        </div>

        <div class="card bg-base-100 shadow-xl mt-8">
            <div class="card-body">
                <h2 class="card-title">说明</h2>
                <div class="py-2">
                    <ul class="list-disc list-inside space-y-2">
                        <li>导出的文件将被压缩为 ZIP 格式。</li>
                        <li>导出操作可能需要一些时间，取决于文件数量和大小。</li>
                        <li>如果遇到问题，请刷新页面重试或联系系统管理员。</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>