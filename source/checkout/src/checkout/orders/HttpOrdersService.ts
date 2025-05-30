/**
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

import { Checkout } from '../models/Checkout';
import { ExistingOrder, OrdersApi } from '../../clients/orders/api';
import { IOrdersService } from './IOrdersService';

export class HttpOrdersService implements IOrdersService {

  private ordersApi : OrdersApi;

  constructor(endpoint: string) {
    this.ordersApi = new OrdersApi(endpoint);
  }

  async create(checkout : Checkout) : Promise<ExistingOrder> {
    return this.ordersApi.createOrder({
      email: checkout.request.customerEmail,
      firstName: checkout.request.shippingAddress.firstName,
      lastName: checkout.request.shippingAddress.lastName,
      items: checkout.request.items.map(item => {
        return {
          price: item.totalCost,
          productId: item.id,
          quantity: item.quantity,
        };
      }),
    }).then((value) => {
      return value.body;
    });
  }
}