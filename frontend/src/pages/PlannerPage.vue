<template>
    <div class="p-6 space-y-6">
        <!-- Header -->
        <div class="flex items-center justify-between">
            <div>
                <h1 class="text-2xl font-bold text-gray-900">Weekly Planner</h1>
                <p class="text-sm text-gray-600 mt-1">
                    {{ weekDates }}
                </p>
            </div>
            <div class="flex space-x-2">
                <Button 
                    variant="solid" 
                    label="Generate Random Flavours" 
                    icon="shuffle"
                    @click="generateRandomFlavours"
                />
                <Button 
                    variant="solid" 
                    label="Export as PNG" 
                    icon="download"
                    @click="exportToPng"
                />
            </div>
        </div>

        <!-- Planner Table -->
        <div class="overflow-x-auto">  <!-- Added this wrapper div -->
            <div ref="plannerTable" class="bg-white rounded-lg shadow min-w-[800px]">  <!-- Added min-width -->
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase w-32">Activity</th>
                            <th v-for="day in weekDays" :key="day.date" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                <div class="flex items-center justify-between">
                                    <div>
                                        {{ day.name }}<br>
                                        <span class="text-gray-400">{{ day.date }}</span>
                                    </div>
                                    <Switch 
                                        v-model="activeDays[day.date]"
                                        class="ml-2"
                                    />
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="activity in activities" :key="activity">
                            <td class="px-6 py-4">
                                {{ activity }}
                            </td>
                            <td v-for="day in weekDays" :key="day.date" class="px-6 py-4">
                                <template v-if="activeDays[day.date]">
                                    <FormControl
                                        v-if="activity !== 'Shakes Flavours'"
                                        type="autocomplete"
                                        v-model="plannerData[`${activity}-${day.date}`]"
                                        :options="coachOptions"
                                        placeholder="Coach"
                                        class="w-full"
                                    />
                                    <textarea
                                        v-else
                                        v-model="plannerData[`${activity}-${day.date}`]"
                                        placeholder="Enter flavours"
                                        class="w-full min-h-[60px] p-2 text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        rows="2"
                                    ></textarea>
                                </template>
                                <div 
                                    v-else 
                                    class="h-full w-full flex items-center justify-center text-gray-500 bg-gray-50 rounded py-2"
                                >
                                    Day Off
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Flavours List -->
        <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-4">Available Flavours</h2>
            <p class="text-gray-600">
                {{ flavours.join(', ') }}
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Button, FormControl, createListResource, Input, Switch, Badge } from 'frappe-ui';
import html2canvas from 'html2canvas';
import { session } from '@/data/session';

const plannerTable = ref(null);
const plannerData = ref({});
const activeDays = ref({});

const activities = ['Shakes', 'Cleaning', 'Shakes Flavours'];

// Get current week dates
const weekDays = computed(() => {
    const days = [];
    const current = new Date();
    const monday = new Date(current);
    monday.setDate(current.getDate() - current.getDay() + 1);

    for (let i = 0; i < 6; i++) { // Monday to Saturday
        const date = new Date(monday);
        date.setDate(monday.getDate() + i);
        days.push({
            name: date.toLocaleDateString('en-US', { weekday: 'long' }),
            date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        });
    }
    return days;
});

const weekDates = computed(() => {
    const firstDay = weekDays.value[0].date;
    const lastDay = weekDays.value[5].date;
    return `${firstDay} - ${lastDay}`;
});

// Initialize active days
weekDays.value?.forEach(day => {
    activeDays.value[day.date] = true;
});

// Get coaches for dropdown
const coachesResource = createListResource({
    doctype: 'Coach',
    fields: ['name', 'full_name'],
    filters: {
        owner: session.user
    },
    auto: true
});

const coachOptions = computed(() => {
    if (!coachesResource.list.data) return [];
    return coachesResource.list.data.map(coach => ({
        label: coach.full_name,
        value: coach.full_name
    }));
});

const flavours = [
    'Vanilla',
    'Chocolate',
    'Banana',
    'Strawberries',
    'Berries',
    'Cookies',
    'Mint & Chocolate'
];

function generateRandomFlavours() {
    weekDays.value.forEach(day => {
        const shuffled = [...flavours].sort(() => 0.5 - Math.random());
        const combination = shuffled.slice(0, 2).join(' & ');
        plannerData.value[`Shakes Flavours-${day.date}`] = combination;
    });
}

async function exportToPng() {
    if (!plannerTable.value) return;
    
    try {
        // Create a container div
        const container = document.createElement('div');
        container.style.padding = '20px';
        container.style.backgroundColor = 'white';
        
        // Add title
        const title = document.createElement('h2');
        title.style.marginBottom = '16px';
        title.style.fontSize = '18px';
        title.style.fontWeight = 'bold';
        title.textContent = `Weekly Planner (${weekDates.value})`;
        container.appendChild(title);
        
        // Create a new table instead of cloning
        const table = document.createElement('table');
        table.style.width = '100%';
        table.style.borderCollapse = 'collapse';
        table.style.fontFamily = 'Arial, sans-serif';

        // Create header row
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        // Add Activity header
        const activityHeader = document.createElement('th');
        activityHeader.textContent = 'Activity';
        activityHeader.style.padding = '8px';
        activityHeader.style.borderBottom = '1px solid #ddd';
        activityHeader.style.borderRight = '1px solid #ddd';
        activityHeader.style.borderLeft = '1px solid #ddd';
        activityHeader.style.borderTop = '1px solid #ddd';

        headerRow.appendChild(activityHeader);
        
        // Add day headers
        weekDays.value.forEach(day => {
            const th = document.createElement('th');
            th.innerHTML = `${day.name}<br/><span style="color: #666">${day.date}</span>`;
            th.style.padding = '8px';
            th.style.borderBottom = '1px solid #ddd';
            th.style.borderRight = '1px solid #ddd';
            th.style.borderLeft = '1px solid #ddd';
            th.style.borderTop = '1px solid #ddd';
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Create body rows
        const tbody = document.createElement('tbody');
        activities.forEach(activity => {
            const tr = document.createElement('tr');
            
            // Add activity name
            const tdActivity = document.createElement('td');
            tdActivity.textContent = activity;
            tdActivity.style.padding = '8px';
            tdActivity.style.borderBottom = '1px solid #ddd';
            tdActivity.style.borderRight = '1px solid #ddd';
            tdActivity.style.borderLeft = '1px solid #ddd';
            tr.appendChild(tdActivity);
            
            // Add data for each day
            weekDays.value.forEach(day => {
                const td = document.createElement('td');
                td.style.padding = '8px';
                td.style.borderBottom = '1px solid #ddd';
                td.style.borderRight = '1px solid #ddd';

                if (!activeDays.value[day.date]) {
                    td.textContent = 'Day Off';
                    td.style.backgroundColor = '#f3f4f6';
                    td.style.color = '#6b7280';
                    td.style.textAlign = 'center';
                } else {
                    const value = plannerData.value[`${activity}-${day.date}`];
                    // Handle FormControl value object for coaches
                    if (activity !== 'Shakes Flavours' && value) {
                        td.textContent = typeof value === 'object' ? value.label || value.value : value;
                    } else {
                        td.textContent = value || '';
                    }
                }
                
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
        
        table.appendChild(tbody);
        container.appendChild(table);
        
        // Add container to document temporarily
        document.body.appendChild(container);
        
        // Generate PNG
        const canvas = await html2canvas(container, {
            allowTaint: true,
            useCORS: true,
            scale: 2
        });
        
        // Remove temporary container
        document.body.removeChild(container);
        
        // Download PNG
        const image = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = `planner-${weekDates.value}.png`;
        link.href = image;
        link.click();
    } catch (error) {
        console.error('Error exporting planner:', error);
    }
}
</script>