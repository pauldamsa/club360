<template>
    <div class="p-6">
        <!-- Header -->
        <div class="mb-8">
            <h1 class="text-2xl font-bold text-gray-900">Reports</h1>
            <p class="mt-2 text-gray-600">Generate and download club reports</p>
        </div>

        <!-- Filters Section -->
        <Card class="mb-6">
            <div class="p-4 space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <FormControl
                        type="select"
                        label="Report Type"
                        v-model="filters.reportType"
                        :options="reportTypes"
                        placeholder="Select report type"
                    />
                    <FormControl
                        type="date"
                        label="From Date"
                        v-model="filters.fromDate"
                    />
                    <FormControl
                        type="date"
                        label="To Date"
                        v-model="filters.toDate"
                    />
                </div>
                <div class="flex justify-end space-x-2">
                    <Button 
                        variant="outline" 
                        label="Reset" 
                        @click="resetFilters"
                    />
                    <Button 
                        variant="solid" 
                        label="Generate Report"
                        icon="file-text"
                        :loading="generating"
                        @click="generateReport"
                    />
                </div>
            </div>
        </Card>

        <!-- Report Preview Section -->
        <Card v-if="reportData.length > 0">
            <div class="p-4">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-lg font-medium">Report Preview</h2>
                    <Button
                        variant="solid"
                        label="Export to PDF"
                        icon="download"
                        @click="exportToPDF"
                    />
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th v-for="header in tableHeaders" 
                                    :key="header"
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                                >
                                    {{ header }}
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="(row, index) in reportData" 
                                :key="index"
                                class="hover:bg-gray-50"
                            >
                                <td v-for="(value, key) in row" 
                                    :key="key"
                                    class="px-6 py-4 whitespace-nowrap text-sm"
                                >
                                    {{ value }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </Card>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { Card, Button, FormControl, createResource } from 'frappe-ui';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

const filters = ref({
    reportType: '',
    fromDate: '',
    toDate: ''
});

const generating = ref(false);
const reportData = ref([]);

const reportTypes = [
    { label: 'Visits Summary', value: 'visits' },
    { label: 'Members Activity', value: 'members' },
    { label: 'Referrals Overview', value: 'referrals' }
];

const tableHeaders = computed(() => {
    switch (filters.value.reportType) {
        case 'visits':
            return ['Date', 'Member', 'Type', 'Coach'];
        case 'members':
            return ['Member', 'Status', 'Last Visit', 'Total Visits'];
        case 'referrals':
            return ['Member', 'Referrals Count', 'Active Referrals'];
        default:
            return [];
    }
});

// Add report generation resource
const reportResource = createResource({
    url: 'club360.api.generate_report',
    makeParams() {
        return {
            type: filters.value.reportType,
            from_date: filters.value.fromDate,
            to_date: filters.value.toDate
        };
    },
    onSuccess(response) {
        reportData.value = response.data || [];
        generating.value = false;
    },
    onError(error) {
        console.error('Error generating report:', error);
        generating.value = false;
    }
});

function resetFilters() {
    filters.value = {
        reportType: '',
        fromDate: '',
        toDate: ''
    };
    reportData.value = [];
}

function generateReport() {
    generating.value = true;
    reportResource.submit();
}

function exportToPDF() {
    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(16);
    doc.text(`${filters.value.reportType.toUpperCase()} REPORT`, 14, 15);
    
    // Add date range
    doc.setFontSize(11);
    doc.text(`Period: ${filters.value.fromDate} to ${filters.value.toDate}`, 14, 25);
    
    // Generate table
    autoTable(doc, {
        head: [tableHeaders.value],
        body: reportData.value.map(row => Object.values(row)),
        startY: 35,
        theme: 'grid'
    });
    
    // Save PDF
    doc.save(`club360-${filters.value.reportType}-report.pdf`);
}
</script>