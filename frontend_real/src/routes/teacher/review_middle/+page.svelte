<script>
    import { onMount } from "svelte";
    import axios from "axios";

    // 教师用户名
    let username = "";
    let middleReports = []; // 存储中期检查报告列表
    let selectedReport = null; // 当前选中的报告
    let loading = true;
    let detailLoading = false;
    let error = null;
    
    // 教师评审意见和状态
    let teacherComment = "";
    let reportStatus = "待审核"; // 默认状态
    
    // 弹窗控制
    let showDetailModal = false;

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "用户";
            fetchMiddleReports();
        }
    });

    // 获取该教师名下所有中期检查报告
    async function fetchMiddleReports() {
        try {
            loading = true;
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/middledocx/teacher/${username}`);
            middleReports = response.data;
            console.log("获取的中期检查报告列表:", middleReports);
        } catch (err) {
            error = `获取中期检查报告失败: ${err.message}`;
            console.error("获取中期检查报告失败:", err);
        } finally {
            loading = false;
        }
    }

    // 获取中期检查报告详情
    async function fetchReportDetail(studentId) {
        try {
            detailLoading = true;
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/middledocx/teacher/detail/${studentId}`);
            selectedReport = response.data;
            teacherComment = selectedReport.content6 || ""; // 初始化教师评语
            reportStatus = selectedReport.status || "待审核"; // 初始化状态
            showDetailModal = true;
        } catch (err) {
            error = `获取中期检查报告详情失败: ${err.message}`;
            console.error("获取中期检查报告详情失败:", err);
        } finally {
            detailLoading = false;
        }
    }

    // 提交审核结果
    async function submitReview() {
        if (!selectedReport) return;
        
        try {
            const response = await axios.put(`http://127.0.0.1:8000/api/v1/middledocx/teacher/${selectedReport.student_id}`, {
                status: reportStatus,
                content6: teacherComment
            });
            
            console.log("审核结果提交成功:", response.data);
            
            // 更新本地列表中的状态
            const index = middleReports.findIndex(report => report.student_id === selectedReport.student_id);
            if (index !== -1) {
                middleReports[index].status = reportStatus;
            }
            
            // 关闭弹窗
            showDetailModal = false;
            
            // 刷新列表
            fetchMiddleReports();
        } catch (err) {
            error = `提交审核结果失败: ${err.message}`;
            console.error("提交审核结果失败:", err);
        }
    }

    // 关闭弹窗
    function closeModal() {
        showDetailModal = false;
        selectedReport = null;
    }
    
    // 获取状态标签样式
    function getStatusBadgeClass(status) {
        switch (status) {
            case '通过': return 'badge-success';
            case '不通过': return 'badge-error';
            case '修改后重新提交': return 'badge-warning';
            default: return 'badge-info';
        }
    }
    
    // 格式化日期显示
    function formatDate(dateString) {
        if (!dateString) return '未知时间';
        const date = new Date(dateString);
        return date.toLocaleString();
    }
</script>

<div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">审核学生中期检查报告</h1>
    
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
    {:else if middleReports.length === 0}
        <div class="alert alert-info shadow-lg">
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>暂无学生提交中期检查报告。</span>
            </div>
        </div>
    <!-- 中期检查报告列表 -->
    {:else}
        <div class="overflow-x-auto">
            <table class="table w-full">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>学生ID</th>
                        <th>学生姓名</th>
                        <th>论文题目</th>
                        <th>提交时间</th>
                        <th>审核状态</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    {#each middleReports as report, index}
                        <tr class="hover">
                            <td>{index + 1}</td>
                            <td>{report.student_id}</td>
                            <td>{report.student_name}</td>
                            <td class="max-w-xs truncate" title={report.title}>{report.title}</td>
                            <td>{formatDate(report.created_time)}</td>
                            <td>
                                <span class="badge {getStatusBadgeClass(report.status)}">{report.status || '待审核'}</span>
                            </td>
                            <td>
                                <button 
                                    class="btn btn-primary btn-sm"
                                    on:click={() => fetchReportDetail(report.student_id)}
                                >
                                    查看详情
                                </button>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
    
    <!-- 详情弹窗 -->
    {#if showDetailModal && selectedReport}
        <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div class="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
                <!-- 弹窗头部 -->
                <div class="p-4 border-b sticky top-0 bg-white flex justify-between items-center">
                    <h2 class="text-xl font-semibold">中期检查报告详情</h2>
                    <button class="btn btn-sm btn-circle" on:click={closeModal}>✕</button>
                </div>
                
                {#if detailLoading}
                    <div class="flex justify-center items-center h-64">
                        <span class="loading loading-spinner loading-lg text-primary"></span>
                    </div>
                {:else}
                    <div class="p-6 space-y-6">
                        <!-- 基本信息 -->
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg">
                            <div>
                                <p><span class="font-semibold">学生姓名:</span> {selectedReport.student_name}</p>
                                <p><span class="font-semibold">学生ID:</span> {selectedReport.student_id}</p>
                            </div>
                            <div>
                                <p><span class="font-semibold">提交时间:</span> {formatDate(selectedReport.created_time)}</p>
                                <p><span class="font-semibold">状态:</span> {selectedReport.status || '待审核'}</p>
                            </div>
                            <div class="col-span-1 md:col-span-2">
                                <p><span class="font-semibold">论文题目:</span> {selectedReport.title}</p>
                            </div>
                        </div>
                        
                        <!-- 报告内容 -->
                        <div class="space-y-4">
                            <div class="border rounded-md overflow-hidden">
                                <div class="bg-gray-100 p-3 font-medium">一、设计（论文）的进展情况：（课题工作量是否适中、已完成任务、未完成任务、完成课题存在问题和解决办法）</div>
                                <div class="p-4 whitespace-pre-wrap">{selectedReport.content1 || '无内容'}</div>
                            </div>
                            
                            <!-- 如果中期报告有 content7 字段 -->
                            {#if selectedReport.content7}
                                <div class="border rounded-md overflow-hidden">
                                    <div class="bg-gray-100 p-3 font-medium">备注</div>
                                    <div class="p-4 whitespace-pre-wrap">{selectedReport.content7 || '无内容'}</div>
                                </div>
                            {/if}
                        </div>
                        
                        <!-- 教师评审部分 -->
                        <div class="border rounded-md p-4 space-y-4">
                            <h3 class="font-semibold text-lg">教师审核</h3>
                            
                            <!-- 审核状态选择 -->
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-medium">审核状态</span>
                                </label>
                                <select class="select select-bordered w-full" bind:value={reportStatus}>
                                    <option value="通过">通过</option>
                                    <option value="不通过">不通过</option>
                                    <option value="修改后重新提交">修改后重新提交</option>
                                    <option value="待审核">待审核</option>
                                </select>
                            </div>
                            
                            <!-- 教师评语 -->
                            <div class="form-control">
                                <label class="label">
                                    <span class="label-text font-medium">教师意见：</span>
                                </label>
                                <textarea 
                                    class="textarea textarea-bordered h-32 p-2 w-full" 
                                    placeholder="请填写对此中期检查报告的意见和建议..."
                                    bind:value={teacherComment}
                                ></textarea>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 弹窗底部操作按钮 -->
                    <div class="p-4 border-t flex justify-end space-x-2 sticky bottom-0 bg-white">
                        <button class="btn btn-ghost" on:click={closeModal}>取消</button>
                        <button class="btn btn-primary" on:click={submitReview}>提交审核结果</button>
                    </div>
                {/if}
            </div>
        </div>
    {/if}
</div>