<script>
    import { onMount } from "svelte";
    import axios from "axios";
    import { tick } from 'svelte';
    import '$lib/style.css';

    let username = "";
    let student_id = 0;
    let base_info = {};
    let loading = true;

    // 终期报告内容
    let content1 = '待填写';
    let content2 = '待填写';
    let content3 = '待填写';
    let content4 = '待填写';

    // 状态管理
    let notification = '';
    let notificationType = '';
    let canDownload = false; // 控制是否可下载
    let canSubmit = false; // 控制是否可提交

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            student_id = localStorage.getItem("student_id");
            getData();
        }
    });

    async function getData() {
        try {
            loading = true;
            const res = await axios.get(`http://127.0.0.1:8000/api/v1/projects/base/student/${student_id}`);
            base_info = res.data;
            
            // 验证基本信息是否完整
            checkCanSubmit();
        } catch (error) {
            console.error('获取基本信息失败:', error);
            notification = '获取基本信息失败，请稍后重试';
            notificationType = 'alert-error';
        } finally {
            loading = false;
        }
    }

    // 验证是否可以提交终期报告
    function checkCanSubmit() {
        // 检查基本信息是否完整
        if (!base_info || !base_info.title || !base_info.teacher_name) {
            notification = '基本信息不完整，无法提交终期报告';
            notificationType = 'alert-warning';
            canSubmit = false;
            return;
        }

        // 通过所有检查
        notification = '';
        canSubmit = true;
    }

    async function handleSubmit() {
        // 再次检查是否可提交
        if (!canSubmit) {
            notification = '基本信息不完整，请确保课题信息已填写完整';
            notificationType = 'alert-warning';
            return;
        }

        try {
            loading = true;
            const response = await axios.post('http://127.0.0.1:8000/api/v1/enddocx/student/create/', {
                title: base_info.title,
                teacher_name: base_info.teacher_name,
                student_name: username,
                student_id: student_id,
                content1,
                content2,
                content3,
                content4
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'accept': 'application/json'
                }
            });

            if (response.status === 200) {
                notification = '终期报告创建成功';
                notificationType = 'alert-success';
                canDownload = true; // 提交成功后允许下载
            } else {
                notification = '终期报告创建失败';
                notificationType = 'alert-error';
            }
        } catch (error) {
            console.error('Error:', error);
            notification = '终期报告创建失败，请稍后重试';
            notificationType = 'alert-error';
        } finally {
            loading = false;
        }
    }

    // 下载终期报告
    async function handleDownload() {
        try {
            loading = true;
            const res = await axios.get(`http://127.0.0.1:8000/api/v1/enddocx/student/download/${student_id}`, {
                responseType: 'blob'
            });

            const contentDisposition = res.headers['content-disposition'];
            let filename = '终期报告.docx';
            if (contentDisposition && contentDisposition.includes('filename')) {
                const match = contentDisposition.match(/filename\*?=['"]?utf-8''([^']+)/);
                if (match && match[1]) {
                    filename = decodeURIComponent(match[1]);
                }
            }

            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            notification = '下载成功';
            notificationType = 'alert-success';
        } catch (error) {
            console.error('下载失败:', error);
            notification = '下载失败，请稍后重试';
            notificationType = 'alert-error';
        } finally {
            loading = false;
        }
    }
</script>

<div class="bg-gray-50 min-h-screen text-gray-800 mt-0 p-2">
    <h2 class="text-xl font-semibold mb-4 mt-0">终期报告填写</h2>

    {#if loading}
        <div class="flex justify-center my-8">
            <span class="loading loading-spinner loading-lg"></span>
        </div>
    {:else}
        <div class="bg-slate-100 p-3 rounded-md mb-4">
            <p class="font-medium mb-2">基本信息</p>
            <div class="flex flex-wrap gap-2">
                <span>题目: {base_info.title || '暂无'}</span>
                <span>|</span>
                <span>指导教师: {base_info.teacher_name || '暂无'}</span>
                <span>|</span>
                <span>学生姓名: {username}</span>
                <span>|</span>
                <span>学号: {student_id}</span>
            </div>
        </div>

        {#if notification}
            <div class={`alert ${notificationType} shadow-lg mt-2 mb-4`}>
                <div>
                    {#if notificationType === 'alert-warning'}
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                    {:else if notificationType === 'alert-success'}
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    {:else}
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    {/if}
                    <span>{notification}</span>
                </div>
            </div>
        {/if}

        <div class="mb-4">
            <label class="block bg-slate-100 p-2 rounded-t-md">一、主要内容</label>
            <textarea class="textarea textarea-bordered w-full h-40 rounded-t-none" bind:value={content1}></textarea>
        </div>

        <div class="mb-4">
            <label class="block bg-slate-100 p-2 rounded-t-md">二、基本要求</label>
            <textarea class="textarea textarea-bordered w-full h-40 rounded-t-none" bind:value={content2}></textarea>
        </div>

        <div class="mb-4">
            <label class="block bg-slate-100 p-2 rounded-t-md">三、进度安排</label>
            <textarea class="textarea textarea-bordered w-full h-40 rounded-t-none" bind:value={content3}></textarea>
        </div>

        <div class="mb-4">
            <label class="block bg-slate-100 p-2 rounded-t-md">四、主要参考文献</label>
            <textarea class="textarea textarea-bordered w-full h-40 rounded-t-none" bind:value={content4}></textarea>
        </div>

        <div class="flex gap-2">
            <button 
                class="btn btn-primary flex-1" 
                on:click={handleSubmit} 
                disabled={!canSubmit || loading}
            >
                {#if loading}
                    <span class="loading loading-spinner loading-sm mr-2"></span>
                {/if}
                提交终期报告
            </button>
            <button 
                class="btn btn-secondary flex-1" 
                on:click={handleDownload} 
                disabled={!canDownload || loading}
            >
                {#if loading && canDownload}
                    <span class="loading loading-spinner loading-sm mr-2"></span>
                {/if}
                下载终期报告
            </button>
        </div>
    {/if}
</div>