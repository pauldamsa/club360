<template>
    <div class="p-6 space-y-6">
        <!-- Total Stock Overview -->
        <Card class="bg-white">
            <div class="p-4">
                <h2 class="text-lg font-medium mb-4">Total Stock Overview</h2>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="p-4 border rounded-lg">
                        <div class="text-sm text-gray-500">Formula 1</div>
                        <div class="text-2xl font-semibold">{{ totalStock.shake || 0 }}</div>
                    </div>
                    <div class="p-4 border rounded-lg">
                        <div class="text-sm text-gray-500">Herbal Tea</div>
                        <div class="text-2xl font-semibold">{{ totalStock.tea || 0 }}</div>
                    </div>
                    <div class="p-4 border rounded-lg">
                        <div class="text-sm text-gray-500">Aloe</div>
                        <div class="text-2xl font-semibold">{{ totalStock.aloe || 0 }}</div>
                    </div>
                    <div class="p-4 border rounded-lg">
                        <div class="text-sm text-gray-500">PDM</div>
                        <div class="text-2xl font-semibold">{{ totalStock.pdm || 0 }}</div>
                    </div>
                </div>
            </div>
        </Card>

        <!-- Stock Per Coach -->
        <Card>
            <div class="p-4">
                <h2 class="text-lg font-medium mb-4">Stock Per Coach</h2>
                <div class="overflow-x-auto">
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
                                <td class="px-6 py-4">{{ coach.stock?.shake || 0 }}</td>
                                <td class="px-6 py-4">{{ coach.stock?.tea || 0 }}</td>
                                <td class="px-6 py-4">{{ coach.stock?.aloe || 0 }}</td>
                                <td class="px-6 py-4">{{ coach.stock?.pdm || 0 }}</td>
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
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead>
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Coach</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="entry in stockHistory" :key="entry.name">
                                <td class="px-6 py-4">{{ formatDate(entry.date) }}</td>
                                <td class="px-6 py-4">{{ entry.coach_name }}</td>
                                <td class="px-6 py-4">{{ entry.product }}</td>
                                <td class="px-6 py-4">
                                    <Badge 
                                        :label="entry.quantity" 
                                        :variant="entry.quantity > 0 ? 'solid' : 'danger'"
                                    />
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
import { createListResource, Card, Badge } from 'frappe-ui';

// Get stock history
const stockHistoryResource = createListResource({
    doctype: 'Stock Entry',
    fields: ['name', 'date', 'coach', 'coach_name', 'product', 'quantity'],
    orderBy: 'date desc',
    auto: true
});

const stockHistory = computed(() => stockHistoryResource.list.data || []);

// Get coaches with their stock
const coachStockResource = createListResource({
    doctype: 'Coach',
    fields: ['id_herbalife', 'full_name', 'stock'],
    auto: true
});

const coachStock = computed(() => coachStockResource.list.data || []);

// Calculate total stock
const totalStock = computed(() => {
    const totals = { shake: 0, tea: 0, aloe: 0, pdm: 0 };
    coachStock.value.forEach(coach => {
        if (coach.stock) {
            totals.shake += coach.stock.shake || 0;
            totals.tea += coach.stock.tea || 0;
            totals.aloe += coach.stock.aloe || 0;
            totals.pdm += coach.stock.pdm || 0;
        }
    });
    return totals;
});

function formatDate(date) {
    return new Date(date).toLocaleDateString();
}
</script>