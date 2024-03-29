# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> tokenB->tokenA->tokenD->tokenC->tokenB;
> 5->5.655322->2.458781->5.088927->20.129889;
> 20.129889

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> slippage 指用戶執行交易時預期價格與實際成交價格之間的差異。slippage 通常由市場價格波動引起，在大額交易或流動性較低的市場中更為常見。
> Uniswap V2 透過使用"最小接收量"（minimum amount received）機制來解決 slippage 問題。當使用者執行交易時，他們可以指定一個最低接收量的閾值。如果實際交易的結果低於這個閾值，交易會被 rollback，從而保護用戶免受不利的價格變化影響。這個機制要求使用者在執行交易前對 slippage 有一定的預期，並據此設定可接受的最低值。

```solidity
function swapTokens(
    address inputToken,
    address outputToken,
    uint256 inputAmount,
    uint256 minOutputAmount
) public {
    uint256 outputAmount = getOutputAmount(inputToken, outputToken, inputAmount);
    
    // 檢查實際輸出量是否滿足使用者設定的最小輸出量要求
    require(outputAmount >= minOutputAmount, "Slippage too high");

    // 執行交易邏輯...
}
```

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> 在Uniswap V2及其許多分叉和類似的自動做市商（AMM）協議中，當首次向一個新的交易對池添加流動性時，會有一定數量的流動性代幣被永久鎖定或「燒毀 」。 這主要是出於兩個原因：
>
> 1. 防止除以零錯誤當第一次為一個交易對池添加流動性時，池中還沒有任何流動性代幣（LP tokens），因此基於池中現有 流動性來計算應該鑄造多少新的流動性代幣的公式可能導致除以零的情況。 為了避免這種情況，協議先鎖定一小部分流動性代幣，確保後續流動性提供者鑄造代幣的計算不會遇到除以零的錯誤。
> 2. 初始價格設定 Uniswap V2 允許流動性提供者自由設定一個新池的初始價格。 這是透過他們添加的兩種代幣的相對比例來實現的。 鎖定最小流動性確保池中有一個非零的、穩定的初始價格基準，從而幫助防止在交易開始時可能出現的操縱或極端價格波動。 最小流動性機制 Uniswap V2 在初始鑄造時從流動性代幣中減去的確切數量是 MINIMUM_LIQUIDITY，通常設定為1000個流動性代幣。 這些代幣被送到合約地址（例如，0x00...dead），從而永久地將它們從流通中移除。

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> 這個設計的主要目的是保持公平性和比例一致性：
>
> 1. 公平性：確保新加入的流動性提供者獲得的流動性代幣數量與他們對池中現有流動性的貢獻成正比。 這意味著無論何時加入，流動性提供者的份額都反映了他們對池子的實際貢獻。
> 2. 價值保存：防止透過存入不匹配的代幣比例來操縱池子價值或流動性代幣價值。 使用這個公式，存入的代幣比例必須與池中現有的代幣比例大致相匹配，從而維持了池中代幣價值的穩定性。
> 3. 價格影響：當流動性提供者向池中添加代幣時，他們實際上是按照當前的市場價格（由池中的代幣比例決定）進行操作的。
>
> 這個機制確保了流動性的添加不會對現有的市場價格產生不公正的影響。 透過這種方式，Uniswap V2鼓勵流動性的添加同時維護了現有投資者的利益和市場的穩定性。 每個流動性提供者的利益都與他們提供的流動性成正比，無論他們是在池子剛創建時加入還是在市場已經成熟後加入。

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

> 三明治攻擊（Sandwich Attack）是在去中心化金融（DeFi）領域中一種常見的惡意操作，特別是在自動做市商（AMM）如Uniswap中。這種攻擊通常針對普通用戶正在試圖執行的交易。
>
> #### 三明治攻擊的運作方式
>
> 1. 預備階段：攻擊者監控待處理交易（mempool）中的交易，尋找一個有利可圖的交易目標，例如一個大額的代幣兌換請求。
> 2. 前置交易：攻擊者在目標交易之前快速地執行一個同方向（買入或賣出）的交易，以提高目標代幣的價格（對於買入操作）或降低其價格（對於賣出操作）。
> 3. 目標交易：普通用戶的交易隨後被執行，但由於市場價格已經被攻擊者的前置交易影響，用戶會以較不利的價格完成交易。
> 4. 後置交易：攻擊者再執行一個與前置交易相反方向的交易，利用市場價格回調，從而賺取差價。
>
> #### 對用戶的影響
>
> 當你嘗試發起交換時，三明治攻擊可能會對你造成以下影響：
>
> 1. 成本增加：你可能會以比正常市場條件更差的價格完成交易，因為攻擊者的前置交易已經人為地推高或降低了代幣的價格。
> 2. 滑點加劇：即使設定了滑點保護，大額交易仍可能受到顯著影響，導致實際交易價格與預期有較大偏差。
> 3. 損失資金：在極端情況下，如果市場對該代幣的流動性不足，三明治攻擊可能導致你的交易產生顯著損失。

