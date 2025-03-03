<template>
    <div class="p-4 md:p-6 space-y-4 md:space-y-6">
        <!-- Total Stock Overview -->
        <Card class="bg-white">
            <div class="p-4">
                <h2 class="text-lg font-medium mb-4">Total Stock Overview</h2>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
                    <div class="p-3 md:p-4 border rounded-lg">
                        <div class="text-sm text-gray-500">Formula 1</div>
                        <div class="text-xl md:text-2xl font-semibold">{{ totalStock.shake || 0 }}</div>
                    </div>
                    <div class="p-3 md:p-4 border rounded-lg">
                        <div class="text-sm text-gray-500">Herbal Tea</div>
                        <div class="text-xl md:text-2xl font-semibold">{{ totalStock.tea || 0 }}</div>
                    </div>
                    <div class="p-3 md:p-4 border rounded-lg">
                        <div class="text-sm text-gray-500">Aloe</div>
                        <div class="text-xl md:text-2xl font-semibold">{{ totalStock.aloe || 0 }}</div>
                    </div>
                    <div class="p-3 md:p-4 border rounded-lg">
                        <div class="text-sm text-gray-500">PDM</div>
                        <div class="text-xl md:text-2xl font-semibold">{{ totalStock.pdm || 0 }}</div>
                    </div>
                </div>
            </div>
        </Card>

        <!-- Stock Per Coach -->
        <Card>
            <div class="p-4">
                <h2 class="text-lg font-medium mb-4">Stock Per Coach</h2>
                
                <!-- Mobile View -->
                <div class="block sm:hidden">
                    <div class="space-y-4">
                        <div v-for="coach in coachStock" 
                             :key="coach.id_herbalife" 
                             class="border rounded-lg p-4"
                        >
                            <div class="mb-3">
                                <div class="font-medium text-gray-900">{{ coach.full_name }}</div>
                            </div>
                            <div class="grid grid-cols-2 gap-3">
                                <div class="text-sm">
                                    <span class="text-gray-500">Formula 1:</span>
                                    <span class="ml-2 font-medium">{{ coach.stock[0]?.servings || 0 }}</span>
                                </div>
                                <div class="text-sm">
                                    <span class="text-gray-500">Tea:</span>
                                    <span class="ml-2 font-medium">{{ coach.stock[2]?.servings || 0 }}</span>
                                </div>
                                <div class="text-sm">
                                    <span class="text-gray-500">Aloe:</span>
                                    <span class="ml-2 font-medium">{{ coach.stock[1]?.servings || 0 }}</span>
                                </div>
                                <div class="text-sm">
                                    <span class="text-gray-500">PDM:</span>
                                    <span class="ml-2 font-medium">{{ coach.stock[3]?.servings || 0 }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Desktop View -->
                <div class="hidden sm:block overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead>
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Coach</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Formula 1</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Herbal Tea</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Aloe</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">PDM</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="coach in coachStock" :key="coach.id_herbalife">
                                <td class="px-6 py-4">{{ coach.full_name }}</td>
                                <td class="px-6 py-4">{{ coach.stock[0]?.servings || 0 }}</td>
                                <td class="px-6 py-4">{{ coach.stock[2]?.servings || 0 }}</td>
                                <td class="px-6 py-4">{{ coach.stock[1]?.servings || 0 }}</td>
                                <td class="px-6 py-4">{{ coach.stock[3]?.servings || 0 }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </Card>

        <!-- Stock History -->
        <Card>
            <div class="p-4">
                <h2 class="text-lg font-medium mb-4">Stock History</h2>
                
                <!-- Mobile View -->
                <div class="block sm:hidden">
                    <div class="space-y-4">
                        <div v-for="entry in stockHistory" 
                             :key="entry.name" 
                             class="border rounded-lg p-4"
                        >
                            <div class="mb-3">
                                <div class="font-medium text-gray-900">{{ entry.coach_name }}</div>
                                <div class="text-sm text-gray-500">{{ formatDate(entry.data) }}</div>
                            </div>
                            <div class="grid grid-cols-2 gap-3">
                                <div class="text-sm">
                                    <span class="text-gray-500">Formula 1:</span>
                                    <span class="ml-2 font-medium">{{ entry.shake || 0 }}</span>
                                </div>
                                <div class="text-sm">
                                    <span class="text-gray-500">Tea:</span>
                                    <span class="ml-2 font-medium">{{ entry.tea || 0 }}</span>
                                </div>
                                <div class="text-sm">
                                    <span class="text-gray-500">Aloe:</span>
                                    <span class="ml-2 font-medium">{{ entry.aloe || 0 }}</span>
                                </div>
                                <div class="text-sm">
                                    <span class="text-gray-500">PDM:</span>
                                    <span class="ml-2 font-medium">{{ entry.pdm || 0 }}</span>
                                </div>
                            </div>
                            <div class="mt-2 text-sm text-gray-500">{{ entry.type_event }}</div>
                        </div>
                    </div>
                </div>

                <!-- Desktop View -->
                <div class="hidden sm:block overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead>
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Coach</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type Event</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Shake</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Aloe</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tea</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">PDM</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="entry in stockHistory" :key="entry.name">
                                <td class="px-6 py-4">{{ formatDate(entry.data) }}</td>
                                <td class="px-6 py-4">{{ entry.coach_name }}</td>
                                <td class="px-6 py-4">{{ entry.type_event }}</td>
                                <td class="px-6 py-4">{{ entry.shake || 0 }}</td>
                                <td class="px-6 py-4">{{ entry.aloe || 0 }}</td>
                                <td class="px-6 py-4">{{ entry.tea || 0 }}</td>
                                <td class="px-6 py-4">{{ entry.pdm || 0 }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Pagination -->
                <div class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 mt-4">
                    <div class="flex flex-1 justify-center sm:justify-between items-center">
                        <div class="flex space-x-2">
                            <Button 
                                variant="outline" 
                                size="sm"
                                :disabled="!stockHistoryResource.hasPreviousPage"
                                @click="stockHistoryResource.previous()"
                                class="w-24"
                            >
                                Previous
                            </Button>
                            <Button 
                                variant="outline" 
                                size="sm"
                                :disabled="!stockHistoryResource.hasNextPage"
                                @click="stockHistoryResource.next()"
                                class="w-24"
                            >
                                Next
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </Card>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { createListResource, Card, Badge, createDocumentResource } from 'frappe-ui';
import { session } from '@/data/session';

// Get list of coaches first
const coachListResource = createListResource({
    doctype: 'Coach',
    fields: ['name', 'id_herbalife', 'full_name', 'role'],
    filters: {
        owner: session.user,
        role: ['in', ['Junior Partner', 'Club Owner']]
    },
    auto: true,
    onSuccess: (data) => {
        // Create individual document resources when coach list loads
        coachResources.value = data.map(coach => ({
            ...coach,
            resource: createDocumentResource({
                doctype: 'Coach',
                name: coach.id_herbalife,
                fields: ['*'],
                auto: true
            })
        }));
    }
});
// Store coach resources
const coachResources = ref([]);

// Update coach stock computed to use document resources
const coachStock = computed(() => {
    return coachResources.value.map(coach => ({
        ...coach,
        stock: coach.resource.doc?.stock || {}
    }));
});

// Update total stock calculation to use new structure
const totalStock = computed(() => {
    const totals = { shake: 0, tea: 0, aloe: 0, pdm: 0 };
    coachStock.value.forEach(coach => {
        if (coach.stock) {
            totals.shake += Number(coach.stock[0]?.servings || 0);
            totals.tea += Number(coach.stock[2]?.servings || 0);
            totals.aloe += Number(coach.stock[1]?.servings || 0);
            totals.pdm += Number(coach.stock[3]?.servings || 0);
        }
    });
    return totals;
});

// Update stock history resource to include pagination
const stockHistoryResource = createListResource({
    doctype: 'Stock Entry',
    fields: ['name', 'data', 'coach', 'type_event', 'shake', 'aloe', 'tea', 'pdm'],
    orderBy: 'data desc',
    filters: {
        owner: session.user
    },
    pageLength: 5,
    pagination: true,
    auto: true
});

// Fix coach name mapping
const coachNames = computed(() => {
    const mapping = {};
    if (coachListResource.list.data) {
        coachListResource.list.data.forEach(coach => {
            mapping[coach.id_herbalife] = coach.full_name;  // Fixed: use id_herbalife as key
        });
    }
    return mapping;
});
// Map coach IDs to names in stock history
const stockHistory = computed(() => {
    return (stockHistoryResource.list.data || []).map(entry => ({
        ...entry,
        coach_name: coachNames.value[entry.coach] || entry.coach
    }));
});

function formatDate(date) {
    return new Date(date).toLocaleDateString();
}
</script>