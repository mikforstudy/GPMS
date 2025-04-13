<script>
    import { onMount } from "svelte";
    import axios from "axios";

    // 教师用户名
    let username = "";
    // 学生过程文档列表
    let studentProcessFiles = [];
    let loading = true;
    let error = null;

    // 展开/折叠控制
    let expandedStudents = {};

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            fetchStudentProcessFiles();
        }
    });

    // 获取该教师名下所有学生的过程文档
    async function fetchStudentProcessFiles() {
        try {
            loading = true;
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/process/teacher/${username}`);
            studentProcessFiles = response.data;
            console.log("获取的学生过程文档列表:", studentProcessFiles);
            
            // 初始化展开状态
            studentProcessFiles.forEach(student => {
                expandedStudents[student.student_id] = false;
            });
        } catch (err) {
            error = `获取学生过程文档失败: ${err.message}`;
            console.error("获取学生过程文档失败:", err);
        } finally {
            loading = false;
        }
    }

    // 下载文件
    async function downloadFile(url, fileName) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000${url}`, {
                responseType: 'blob'
            });
            
            const fileUrl = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = fileUrl;
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(fileUrl);
        } catch (err) {
            error = `下载文件失败: ${err.message}`;
            console.error("下载文件失败:", err);
        }
    }

    // 切换展开/折叠状态
    function toggleExpand(studentId) {
        expandedStudents[studentId] = !expandedStudents[studentId];
    }

    // 格式化日期
    function formatDate(dateString) {
        if (!dateString) return '未知时间';
        return dateString;
    }
</script>

<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">学生过程文档管理</h1>
    
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
    {:else if studentProcessFiles.length === 0}
        <div class="alert alert-info shadow-lg">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>暂无学生提交过程文档。</span>
            </div>
        </div>
    <!-- 学生过程文档列表 -->
    {:else}
        <div class="space-y-4">
            {#each studentProcessFiles as student}
                <div class="card bg-base-100 shadow-md">
                    <div class="card-body p-4">
                        <!-- 学生信息 -->
                        <div class="flex justify-between items-center">
                            <div>
                                <h2 class="card-title text-lg">
                                    学生: {student.student_name} (ID: {student.student_id})
                                </h2>
                                <p class="text-sm text-gray-600 mt-1">论文题目: {student.title}</p>
                            </div>
                            
                            <!-- 展开/折叠按钮 -->
                            <button 
                                class="btn btn-sm btn-circle"
                                on:click={() => toggleExpand(student.student_id)}
                            >
                                {#if expandedStudents[student.student_id]}
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                                    </svg>
                                {:else}
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                                    </svg>
                                {/if}
                            </button>
                        </div>
                        
                        <!-- 文件列表 (可展开/折叠) -->
                        {#if expandedStudents[student.student_id]}
                            {#if student.files && student.files.length > 0}
                                <div class="overflow-x-auto mt-4">
                                    <table class="table w-full">
                                        <thead>
                                            <tr>
                                                <th>文件名</th>
                                                <th>大小</th>
                                                <th>上传时间</th>
                                                <th>操作</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {#each student.files as file}
                                                <tr>
                                                    <td>{file.file_name}</td>
                                                    <td>{file.file_size}</td>
                                                    <td>{formatDate(file.file_ctime)}</td>
                                                    <td>
                                                        <button 
                                                            class="btn btn-sm btn-primary"
                                                            on:click={() => downloadFile(file.download_url, file.file_name)}
                                                        >
                                                            下载
                                                        </button>
                                                    </td>
                                                </tr>
                                            {/each}
                                        </tbody>
                                    </table>
                                </div>
                            {:else}
                                <div class="alert alert-info mt-4">
                                    <div>
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                        <span>该学生暂无提交过程文档。</span>
                                    </div>
                                </div>
                            {/if}
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>