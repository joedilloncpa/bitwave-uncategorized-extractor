import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Wallet lookup dictionary - from wallets-ME.csv
WALLET_LOOKUP = {
    'ZA4cMuS4u5UKHFquLxAd': 'BTC Revenue Share',
    'HUv0Wlvc1LHYSqfA6Dmi': 'BTC Trading Balance',
    'NSKl1EAVPvFK1HoZBLk9': 'BTC Working Capital',
    'X9w9Z1dZjHFdjuEpllrj': 'ETH Trading Balance',
    '9DYSHM7xZ1fRF1TaL0T2': 'FB - Default - SOL Wallet 1 (3epE)',
    'mrjdHeZrj7qi5NHf2y5g': 'FB - Launchpad Referral - BASE Wallet 1 (b75A)',
    'Rvw9dekYzBF31cBqrknI': 'FB - Launchpad Referral - ETH Wallet 1 (b75A)',
    'btq6TdbWeiQzw4yl3y6G': 'FB - Launchpad Revenue - BTC Wallet 1 (0cn5)',
    'JmpcyqvRfiYE59o2C8tK': 'FB - Launchpad Revenue - BTC Wallet 2 (zGaU)',
    'i8gUh0BDpfVuHyUTel84': 'FB - Launchpad Revenue - SOL Wallet 1 (oyrP)',
    'amqWpI7cPoXDn7JIwnr2': 'FB - Lucky Buy - Revenue - SOL Wallet 1 (FiYU)',
    '3svtRVlsVigF6AuYupMy': 'FB - Marketplace Ops Refunds (0x95...a46c)',
    'hKUjdeuCNl2GmkA31jDC': 'FB - Minting Fee - SOL Wallet 1 (xBgF)',
    'MDMNkAd1jzOyHbeCG7fo': 'FB - Referral Royalty - SOL Wallet 1 (PySw)',
    'YDtmCc1bDXtZdNNuHmvE': 'FB - SEI Launchpad Revenue (0x4e...0b68)',
    'OYgAgxUo6eUXWYKePaXx': 'FB - SEI Partnership (0x5fB...2EB4b)',
    'FDqZu95VpPwxNE7MNcVB': 'FB - Secondary Marketplace Fees - ARB Wallet 4 (F27E)',
    'rohILCJVyvBKo1ytIaap': 'FB - Secondary Marketplace Fees - BASE Wallet 4 (F27E)',
    'mUVQ8EYqQoEGwzpQp2I6': 'FB - Secondary Marketplace Fees - BSC Wallet 4 (F27E)',
    'SMLZKt6HoRo8RhvU8lia': 'FB - Secondary Marketplace Fees - BTC Wallet 1 (n0gs)',
    'meY3L7WS4ovzrUE63chV': 'FB - Secondary Marketplace Fees - BTC Wallet 2 (Hzmj)',
    'GWPD1j45GpmmYm0e9LeC': 'FB - Secondary Marketplace Fees - ETH Wallet 4 (F27E)',
    'pT5fsoYawpy7YtAhvH82': 'FB - Secondary Marketplace Fees - POLY Wallet 4 (F27E)',
    'MYKDMbWZnSEeVQdZmXEG': 'FB - Secondary Marketplace Fees - SOL Wallet 1',
    'L9B7U6AcspJqgV5pXcKw': 'FB - Secondary Marketplace Fees SEI',
    'S02lqhcF02X8yft4ltXX': 'FB - T2 Swaps Vault (Henn9...BDux9)',
    'lr7Ooreq8JahY9lY9Kp1': 'FB - Working Capital - BASE Wallet 2 (2850)',
    'mGXlPsthlHQc6lujYGrA': 'FB - Working Capital - ETH Wallet 2 (2850)',
    '9JcbGvdmYHUFxn75z88G': 'FB - Working Capital - SEI (2850)',
    'nv6cqu6esAEqzXQSzTI6': 'FB - Working Capital - SOL Wallet 1 (nbEB)',
    'rsAv9AKkiOtMsDRPVxTs': 'Gg5j2ziwiF8T7sFTKx47ZavgXNDC3XXTcvh1cy2FvkDx',
    'k5wD9GknRGux18tQpqyM': 'Internal Swap Wallet BASE',
    'rztnAn4qXSVqk7PYZoxU': 'Internal Swap Wallet ETH',
    '8gePQ4nqNep8Y7OSNm4f': 'Internal Swap Wallet MATIC',
    'kVGG0HQoBXBkQ9czC6vg': 'Keiko Community (Unlocked)',
    'vOqaadCNmOFVxoaZ9Pbn': 'Keiko Insider (Locked)',
    '0845328d-48af-4f09-85bc-6056adb2824b': 'LBR - CBP',
    '27cpQf7n9kxMoCzJoXON': 'Lucky Buy - Revenue',
    'HnlXDrhkYnsyzdVx0Ude': 'Lucky Buy - Revenue - Base',
    'dmo8EiaHL3d0eHCUIrBh': 'ME SOL Validator',
    'PJV2tMI6n8vkihgJJglH': 'ME SOL Validator Treasury (B7XL...dVF3)',
    'FqnX6SiVMuheSxmH7Rso': 'ME Trading Wallet',
    'gHVr3fORbpeintCRm7az': 'Magic Eden Validator (Vote Account)',
    'DSB3q0PzXL3qrWTtakRJ': 'Magic Eden Validator (Withdraw)',
    'iWsksSQzHDC6OVzc9aOU': 'Magic Eden Validator (identity)',
    'iD1jmyIUinaxIsc35JQh': 'NFT Buyback Hot Wallet SOL',
    'yj0WCDqU3dyUySPDCiba': 'New ETH Lucky Buy (0x99...4e1f1)',
    'aoLqhYqvv7a2wild8WNs': 'Payments to ME',
    'eMhxv8o7PKQMVV1I7qF5': 'Payments to ME (0xfEBa...ca8Ff)',
    'yUzZ1nTzVM7Co9yq2jCa': 'SEI Trading Balance',
    'sfF5jNr7o4I6bvOQBKTi': 'SOL Self-Stake',
    'mMe8QfoEbzS85EtDA2zC': 'SOL T2 Internal Vault (EUgN...mZEi1)',
    'Qja2bF2bInbrxMOhu30h': 'SOL Trading Balance',
    'NhJS669vgDS6Jm3onGDB': 'Swap - ETH (DECa)',
    'Irhd0Wn5MKDpISP2FTWw': 'Swap - POLY (2850)',
    'SQYPLkEHbOG3pRRkLjcg': 'Swap - POLY (DECa)',
    'YFSOZnti6tJ8rOB20glE': 'T2 Revenue - Mobile',
    'rnd4TuHYMIjCZ35VNGNW': 'T2 Revenue - Web',
    'hnaaCAsvSWjDdxEPyh85': 'TRUMP Trading Balance',
    'wB5nvPvJgI5UxPMcdBHd': 'USD Trading Balance',
    'R4h5629itjvmT66v7eCn': 'USDC (SOL) Revenue Share',
    '142KkYhARb3Z23y20c71': 'USDC Trading Balance',
    'y4xm2xgJVWUreXq07i5M': 'USDT Trading Balance',
    'VgWMem4mFUj75nmL2Bex': 'zerebro partnership',
    '54TuSJpq1aawE6QqdWwT': '(Base) BaseETH to USDC Conversions',
    'EWRBl2BCOOGBzrffGrAo': '(Base) Launchpad Revenue',
    'kcRfYi65M0fZeYX89lNd': '(Base) Magic Ventures Inc.',
    'Dys0u3pIZ5D28wLFZyM3': '(Base) Magic Ventures LLC',
    'LFdCzVLPg7DIk0WAPeq4': '(Base) Royalties',
    '6zhPVCOoNV2V5l31d8vp': '(Base) Secondary Marketplace Fees',
    'wL6RBQpwcGOrWSltO3Tl': '(arb) Secondary Marketplace Fees',
    'fQ7kss2z3DTBRYp1tlka': '(arb) Working Capital Euclid Labs',
    'bZV3InvvONGTQRlEAgcY': '(base) Launchpad Referral',
    'fENF1KY5lvebZXXklgxv': '(base) Polygon Grant',
    '8bTEiq8W6K0S1OViiaXc': '(base) Working Capital Euclid Labs',
    'u3SXQr38DzYSVN19fyog': '(bsc) Secondary Marketplace Fees',
    'CPhFPVWB8FooeCiKqI0a': '(eth) Internal Swap Wallet',
    'MLZkZMaDa2GdirZ8veCb': '(eth) Launchpad Referral',
    'uxcSmb6iksXjNGOUJprw': '(eth) Revenue Share',
    '98CyJj7rhROr7YXweypl': '(eth) T2 Revenues - Mobile',
    'TtILHhLVH0tK37W7wgam': '(matic) Launchpad Referral',
    'HdS2NSSWIjJKqqOCVU4e': 'ARB Trading Balance',
    'RL8bp3BLzADWMSjY8QSm': 'Accounts Receivable V2',
    'DQ49PJAEZEji1P1S13wG': 'Arbitrum Magic Ventures Inc.',
    'TOwOXjTPs1bjCsQYuub1': 'Arbitrum Magic Ventures LLC',
    '0MiaivbGFtOp112NbdQU': 'Avalanche (C-Chain) External Funding',
    'UqLBVCx1Mvbg2bWOrgO9': 'Avalanche (C-Chain) Magic Ventures Inc.',
    'Z3CrzEatD61KUUxankGC': 'Avalanche (C-Chain) Magic Ventures LLC',
    'rMtP5M0iuuYYiMe35izr': 'BNB Smart Chain Magic Ventures Inc.',
    '4tqOWlFH2QAKNI74TMm3': 'BNB Smart Chain Magic Ventures LLC',
    'W1zYYb50kaNfnxM6ffAJ': 'BTC - bc1qcq2uv5nk6hec6kvag3wyevp6574qmsm9scjxc2',
    '4h3Mt77f47VN2YWzsGEa': 'BTC Trading Balance',
    'zzXmCxgjslBIjk4RyIJ2': 'BTC Trading Balance - Manual',
    'fhvQk0kEtnEr9u9vy3Fy': 'BTC Wallet',
    'jN9JZYf4aZJrpc8kF4Zd': 'Bitcoin Accounts Receivable',
    'rKH4YgYWRp0HZVLUkQMo': 'Bitcoin Accounts Receivable',
    'NSTdlTEjKZAMyghlVnDa': 'Bitcoin BTC UTXO Consolidation Vault',
    'byT2tzz4tcIgqmCdS8Dq': 'Bitcoin BTC UTXO Consolidation Vault',
    'jdgFJo6rwelUbfm3EApJ': 'Bitcoin Helio Rev Share',
    'iSbITRahNZC1Ps8CSvLD': 'Bitcoin Helio Rev Share (2)',
    'QRZmzxYWXTypNDk4zUg6': 'Bitcoin Inscription Tool Fee',
    'qqCc3TPzY1MlSY25Z8Yg': 'Bitcoin Inscription Tool Fee (2)',
    'FvyejErzwrHsAiCgFiQm': 'Bitcoin Launchpad Revenue',
    '8UDRzhbTOkwCA8JoVvlZ': 'Bitcoin Launchpad Revenue (2)',
    'iT7ZKZj8SQK4EZUV40gE': 'Bitcoin Network Deposits',
    'oGZqmmDz8TUYvpibYKEe': 'Bitcoin Network Deposits',
    'DcejJ4tZboiTV8MJDMKR': 'Bitcoin Revenue Share',
    'X4Bz4s2yys0SzHxyYXnE': 'Bitcoin Revenue Share',
    'eytuXf7tfHE1TOZTrSp3': 'Bitcoin Secondary Marketplace Fees',
    'DRqfuL538T1luVkOjSCr': 'Bitcoin Treasury',
    'INrkpjwefl2VXjYrePOH': 'Bitcoin Treasury',
    '5Cupe0jJ9GPLP14k8ANz': 'Bitcoin Working Capital Euclid Labs',
    'JnWKZsREum0ziPNoNdk8': 'Bitcoin Working Capital Euclid Labs',
    'SqZBt6xgPdDPI26yPS1D': 'Celo Magic Ventures Inc.',
    'rbYNqpXwh735WaCvJxUw': 'Celo Magic Ventures LLC',
    '6ca259b6-c6aa-41ae-9e20-86f213cc8cf4': 'CoinbasePrime',
    'JN8BaYRD5wpyUKzIkdRK': 'EPL-BTC Auctions-BTC',
    'hMi1rZCKmSMXIFYMooH2': 'EPL-BTC Auctions-BTC',
    'oB8isTrBJzBh1bfVZAQm': 'EPL-External Funding-ETH',
    'Ac3VaNjXuz0fiLyUqltV': 'EPL-External Funding-MATIC_POLYGON',
    'M0cjHyQgvIA0nXI2hPA8': 'EPL-External Funding-SOL',
    'DnfD9XIgz78SJy1aj7Bn': 'EPL-GP Vault-SOL',
    'DB2eww99BeLEZCDcxOf6': 'EPL-Layer Zero-MATIC_POLYGON',
    'V2xZeLr9Hpxa8SeDQfxv': 'EPL-Lucky Buy - Operational Funding-SOL',
    'mIBatvA1ZYyQX6lbbdN8': 'EPL-Lucky Buy - Revenue-SOL',
    'vMi8XtTCfa4czg2RNNeU': 'EPL-Lucky Buy - Treasury-SOL',
    'eHgJybKbnNjsigJDePLH': 'EPL-MMM-SOL',
    '5qwArqSrn6uNwy2q417A': 'EPL-Magic Eden VIP - Revenue-BTC',
    'jvRtv41imuBN9Jz6v3Vi': 'EPL-Magic Eden VIP - Revenue-BTC',
    'g2AVLzDuKFX2tENfkiwG': 'EPL-Magic Eden VIP - Revenue-ETH',
    '9u6SvDBw9AC20DQAu9OE': 'EPL-Magic Eden VIP - Revenue-MATIC_POLYGON',
    'OiDo6xMf8WTTPU8CKPSp': 'EPL-Magic Eden VIP - Revenue-SOL',
    'RZgMQPHJgFQW99ntVPUX': 'EPL-Minting Fee-BASECHAIN_ETH',
    'TkV4bhpmaTh5hVesNWt5': 'EPL-Minting Fee-ETH',
    'gYQOnjRi3f9zpPA8sQGA': 'EPL-Minting Fee-MATIC_POLYGON',
    'iUgQU4tbgvY6T9U4HAhX': 'EPL-Minting Fee-SEI',
    'hAj3wJZEiJI8w2hxOHNs': 'EPL-Minting Fee-SOL',
    'Kys4y5yNmpTpd97aqerh': 'EPL-Network Deposits-BTC',
    'lUBtad2ypcuYZbAV1Phd': 'EPL-Network Deposits-BTC',
    'qOzkAIcvOFkAGJUKQT91': 'EPL-Network Deposits-BTC',
    'anIvz4lT4rWTr29FnMMg': 'EPL-Network Deposits-BTC-2',
    '6jvLxFPaOIFjNOdROnYA': 'EPL-Network Deposits-BTC-3',
    'M9MO2lCUuQKXfToSgPpq': 'EPL-Network Deposits-BTC-4',
    'NxeNMTYTuWTjlrGzzNqa': 'EPL-Network Deposits-ETH',
    'yMZze48Z6aXle3WE0iCp': 'EPL-Network Deposits-MATIC_POLYGON',
    'XLpmUNLGSDqCkfuDf0Me': 'EPL-Treasury-BTC',
    'ZHM7N2dqBPfvyRd3wvGa': 'EPL-Treasury-BTC',
    'e24YqHWiqZSOqE9Ca2wR': 'EPL-Treasury-ETH',
    'YKT60wD0x0Rp6OnEO0s4': 'EPL-Treasury-MATIC_POLYGON',
    'OE1Z8wVRhllhZQqZLlZD': 'EPL-Treasury-SOL',
    'W9EVJaijFvq0U82lBccL': 'EPL-Working Capital-BTC',
    'iEa5n1UnV6JyejpPuR7v': 'EPL-Working Capital-BTC',
    'Mht7AOW5fox1Ik0DUo4y': 'EPL-Working Capital-ETH',
    'Rk5dioJYZCdbkXlFsvnQ': 'EPL-Working Capital-MATIC_POLYGON',
    'RSwLtZX34ZRwaydMXidv': 'EPL-Working Capital-SOL',
    '22wlH8P8dybN4bAaHgxX': 'ETH Staking Wallet',
    'RpY7NFjUFyXYEPrnMv0C': 'ETH Trading Balance',
    'BoUdLvD80ImrKz4073Qh': 'ETH Wallet',
    'i8Aqb5GxsLYwvJc6Mij8': 'Ethereum Accounts Receivable',
    'vhsuX4Lg7D67PC6tVJEA': 'Ethereum Customer Support Team',
    'RktsWQm8wRMmu4WYMoeg': 'Ethereum Digital Asset Purchase SPV I LLC',
    'so3sfaZsFZyRwtv3HzTe': 'Ethereum ETH Contract Authority',
    'OLx8vsU046Myih6Go7B7': 'Ethereum External Funding',
    'luxma5xeUdA9EZVtnIzT': 'Ethereum Helio Rev Share',
    'g4idTtU1JWpBMPQo0p1K': 'Ethereum Launchpad Ops Team',
    'PSom3QR0Cih3Jn2QL1q6': 'Ethereum Launchpad Revenue',
    'YYVLZlFmbVKqGgwFCtSm': 'Ethereum Magic Ventures Inc.',
    '034kDRAWdcjX0SJ5FUkX': 'Ethereum Magic Ventures LLC',
    'vNNolwiZR026Bam8YDdq': 'Ethereum Network Deposits',
    'I3wUCQjKFXL4DOWucona': 'Ethereum Polygon Grant',
    '8hsFcfl46NYrM17f6SFT': 'Ethereum Royalties',
    'IyTGdpf1njyheBr02oij': 'Ethereum Secondary Marketplace Fees',
    'Qt6eTPNnPdPcDmAVsi18': 'Ethereum Treasury',
    'R1BQbrQFT2E8ggnufJ6n': 'Ethereum Working Capital Euclid Labs',
    'saYGo4IakZgBuvGc8CTV': 'Ethereum [OC - Rev] ETH Launchpad - Ledger',
    '1qlcTm23Sy1kffWGDCOO': 'Ethereum [OC] Ape Coin Holding Wallet',
    's9Yh5SSrEDgBBnaNiWRq': 'Ethereum [OC] ME ERC-20 Opex Wallet',
    't9repv8cHycGkfNQk9tN': 'Euclid Insider (Locked)',
    'RNX8rPWRwFg0cAjh9Xxl': 'Euclid Labs Inc SOL',
    'G8v6nJXZdfcgtdzQ6pbl': 'Euclid Labs Inc USDC',
    'r57qTW4VDrYNVRvSB9iT': 'External Funding V2',
    'Q9XaMI3YimM5e4oldmMW': 'FTX - OPEX',
    'cJqXqNId3KHUiXnRzOoV': 'Fantom Magic Ventures Inc.',
    '7QBxNPQkGmR2sMCqtgZm': 'Fantom Magic Ventures LLC',
    'qfWYt4Ad3LOqAPKrKRNi': 'Gnosis Signing Wallet Joe Doll',
    'GZwCd5DCyC32pRiwJd1e': 'Gnosis Signing Wallet Johannes',
    'FDlB7b1sJQkFl0Cga8gk': 'Gnosis Wallet',
    'RODPJH1J1HQLGIbjtTcM': 'Helio Rev Share V2',
    '7b4bc4ab-5926-48ea-9d09-6120669bff74': 'Kraken',
    'WKrcoJOnZspyyMOJjtO4': 'Launchpad Funding Wallet',
    'Vv8oOYPHJUYh65aWn7mX': 'Launchpad Revenue V2',
    'e95jg28RbULBluTb8uEp': 'Lucky Buy Notary',
    'WcqKDGNxJ4Xwvc4Lf3x9': 'ME Investments (SPL)',
    '3yUFjqukcaxvHGLJjtxr': 'ME Trading Wallet',
    '7eRTHGxAiaAxxjnymfgd': 'MM Testing 1',
    'MJwyjnHOmSwqlwSf5n0Y': 'Optimism Magic Ventures Inc.',
    'VYdEE7PToNv77PKslrUv': 'Optimism Magic Ventures LLC',
    'acO3LvO5prHFkSAfQsX0': 'Polygon External Funding',
    'SOU3dU5jnCm026STCOR0': 'Polygon Helio Rev Share',
    'DrLHb1M1lmw1tyhi7Xad': 'Polygon Launchpad Ops Team',
    '28zbioekTmrjC1vxve2p': 'Polygon Launchpad Revenue',
    'xwYFpbzkqySMeXkjEoaJ': 'Polygon Magic Ventures Inc.',
    'Py2pjsWzsFO5HM2eWIPl': 'Polygon Magic Ventures LLC',
    'H2DM7hzlWDMeFaNLqQKV': 'Polygon Network Deposits',
    'vpg0GroQZmMVFYdFlSa0': 'Polygon Polygon Grant',
    'XExSr5eQWLEd0btBg3LX': 'Polygon Royalties',
    'Xeqgceh38y81q4vUlxW3': 'Polygon Secondary Marketplace Fees',
    'sJNjcvp0AD2zPYEdXt8G': 'Polygon Treasury',
    's3YorU05lmej38CEMHV0': 'Polygon Working Capital Euclid Labs',
    'z5MLeMnszOubihaYYAZs': 'Polygon [FB] A/R - Polygon',
    'Zd9Z6l3aDysmcUtOjybf': 'Polygon [Rev] Polygon Secondary Old-Inactive',
    'RwcsyMxMuMULj322z97s': 'Referral Royalty (Rollup)',
    'yN22GbSYg7TNnoHKGM0l': 'Referral Royalty V2',
    'eJMjTpE3bo79ttcGR5xp': 'SOL Historical Staking Wallet',
    '4uf04CdgccOXiW8tfqez': 'SOL Launchpad Revenue',
    '3MSYXlcRLbkPD0nWLalD': 'SOL Royalty Revenue (Use through 12/31/22) (Sub FTX Wallet)',
    'DISJC41FBmWSOYVCAhpl': 'SOL Staking Wallet',
    '5in7LSZbAVV4LfZSiOPJ': 'SOL Trading Balance',
    '3PihoZoBaSVkHHMvxp4R': 'SOL Trading Balance - Manual',
    're4utPBEQWTFCC3owS0p': 'Secondary Marketplace Fees V2',
    '3O4rn80WVTvtzUkY6CMK': 'Solana Accounts Receivable',
    'webSanYok3xCZ1MdnZD6': 'Solana Customer Support Team',
    'TeH92Nt4yRYHz37jPilW': 'Solana Eng Testing',
    'cZynCMRF92FfNhww43jM': 'Solana External Funding',
    't9slffUVyThiggabAPyz': 'Solana Helio Rev Share',
    'JmQErdPZJoRzKuGxnnPD': 'Solana Launchpad COGS',
    'lHI0VNQWCIow76FzBcIG': 'Solana Launchpad Ops Team',
    'bROLZHy3piu3fboehjh6': 'Solana Launchpad Revenue',
    'sZV0EZQETPCTQdBXTc1R': 'Solana Launchpad Testing Wallet',
    'cbNzt8PygpVLAXnVmUAm': 'Solana Magic Ventures Inc.',
    '5P9az9VstISAHhy2rIAf': 'Solana Magic Ventures LLC',
    'J0yiMMKrM0Vu7ZPkqTga': 'Solana Network Deposits',
    'VuQKY2kGxF0vqa7GDPNT': 'Solana Revenue Share',
    'Z1hoCgMzkqnxfT1OZaf8': 'Solana Revenue Share (Anybodies)',
    'ENCAq5SIeWpqJReSOycF': 'Solana Revenue Share V2',
    'Kfwf1mxz2vyYDYaJ3s4g': 'Solana Royalties',
    'IZ3X59o2bAdCtiXom7KS': 'Solana SOLMaps Revenue',
    'OfHfqiP6rjSSVD2Ws45S': 'Solana Secondary Marketplace Fees',
    'V73TINaPT4Hc4j9TLo3u': 'Solana Treasury',
    'rsv0Ws4BC3crb67cPNke': 'Solana Working Capital Euclid Labs',
    'NLFAaqOE66MEAdQPEtvc': 'Solana Zebec - CS Refunds',
    'IopA9zQMIdUsjAB69d8M': 'Solana Zebec - Launchpad',
    'wPTC9ldkiKtCulKSWvFl': 'Solana [OC] - FB-WL - ME rewards Launch',
    'P3VbnshaypLTtebfdGNd': 'Solana [OC] - FB-WL - Magic Box Reward Wallet 1',
    'lhC29iEHF1KvJri83YGD': 'Solana [OC] - FB-WL - Magic Box Reward Wallet 2',
    'Ay3Z9YgNpxQxwzedEgGF': 'Solana [OC] - FB-WL - Magic Box Reward Wallet 4',
    'g0XR7INgXuGeNTM1ZQP0': 'Stake Accounts 5gaEw875bFhVMryG9VyUR2biyPJq5p5W5MQkfaY8YTQd',
    '91Qha7v6YC4kg72FFi0H': 'Stake Accounts3NXywPy8mZzSKM7er41h1n5BigTcFmY8uWZQy1K4uQoi',
    'E3XVav7Qg7Xje5QgPeCZ': 'Stake Accounts6GWQ8im4wRPhrsbUYxoMeZYEmVBwMxkU4h1VDgXSbTyy',
    '76HWe2tLduUdxGLw200s': 'Stake Accounts82vxLPZaqfnc8ebhjPorBx5sdccmoPoh8NjiK8jpiMnL',
    '83Qy7aATJshp1CUVDGh9': 'Stake Accounts8RaiMVj1sgYtH7VWSyoXyd9q1q8H7HA4wwR9LFAZDJ8j',
    'QqsyabBtuUMwCbrl9GbU': 'Stake Accounts9eGCS7WG31ZKSZhRqYt15vX6FBsYuT9W95Byt5G8WF3Y',
    'yzFnHLyN9xXJYVqInJbe': 'Stake AccountsDvac85S1kMQmVu5KCL1twdD57GCAqrN1hhwvLpVvPtSx',
    'zOgGgusrhBsA43dYLH2R': 'Stake AccountsGSadz1yXKNTNmBg88ykjhiciP4CNwh6TAwSSUkByMupw',
    'CFMuEvi6MS7LbkyZvH8U': 'Stake AccountsGsWNWTxPLcjnyTwHGZtYMVVZggosSjRJBgQ1okv85vhJ',
    'auFJx2rlPGoNMbp5aKEl': 'T2 Revenues - Mobile',
    'lJACKQGfzCAlGeVVPVog': 'T2 Revenues - Mobile V2',
    '0tssn7IrLgGm1vFH8J5H': 'T2 Revenues - Web',
    '1lErtSWIO312U81NxyJD': 'T2 Revenues - Web V2',
    'P9KhJSxMPaPcPSsyjbUp': 'TRUMP Trading Balance',
    'dCr2UkePUki3KmTAAjC6': 'USD Trading Balance',
    'aEeON66QBcmWsRw6Jdsk': 'USDC Trading Balance',
    'Dw7wU2xcj66ttCuMr2dZ': 'USDT Trading Balance',
    'iBWjrTqC0sBMqCqZeY8K': 'Working Capital Euclid Labs V2',
    'SnhY4Vril8YqsaJ98YcR': 'Zebec - Expenses',
    'kISMEY63B8cn4bTVvKHz': '[FB-Ops] Launchpad - Polygon',
    'ZRkcOu6h10rTUpm1oziY': '[FB-Ops] Marketing - Polygon',
    'egMZWNeuyoJXN8q0xqj0': '[FB-Ops] Marketplace Operations - Polygon',
    'MrxTB0lJ0raJ79x0OE4w': '[FB-Ops] Network Deposits - Operations - Ethereum',
    'kWnLC9g0ee6M2KLhod47': '[FB-Ops] Network Deposits - Operations - Polygon',
    'XxEN86l7dmngjLPyDjgs': '[FB] Staking - SOL',
    '8h8mM5WHp4KNVuhUvF4k': '[FTX] FTX US - Bank Transfers',
    'SoenIbIm1fu1WvwzqWej': '[FTX] FTX US - Euclid Labs',
    'eoYrSAdUXtxwk8KRwO53': '[OC] - FB-WL - Magic Box Reward Wallet 3',
    '7DAl5H0qSEtjmrVT68Kb': '[OC] MMM Revenue wallet',
    'xPlQZIw55j2506vgMeT7': '[OC] Marketing - SMB Bids - Terrance Owns',
    'x9RrA3ilPsoGvthitOMu': '[OC] Marketing - SMB Raffle Wallet - Xavier Brown Owns',
    'rlw6IB9sqlWzDrHqUJBW': '[Rev] SOL Launchpad FTX End Nov 2022',
    'tbq0HsFtS4nzh0BdBsDn': '[Rev] SOL MEv1 Secondary Rev (2021 Marketplace-2NZ)',
    '4gGKh30wbgFLE2WzeFCh': '[Rev] SOL MEv2 Secondary (rfq)',
    'qd8UzCntmnEh8ZVpLaUM': '[Rev] SOL Royalty RRUM (source)',
}

def process_crypto_transactions(df):
    """
    Process cryptocurrency transactions according to specified rules
    """
    # Filter for only "Uncategorized" rows
    df = df[df['categorizationStatus'] == 'Uncategorized'].copy()
    
    # Delete specified columns (removed walletId from the list initially, but delete walletName)
    columns_to_delete = [
        'categorizationStatus', 'ordID', 'runId', 'dateTimeSEC', 
        'assetbitwaveId', 'exchangeRateSource', 'exchangeRate', 
        'reconciliationStatus', 'contactId', 'categoryId', 
        'description', 'transactionMetadata', 'linetransactionId',
        'orgId', 'walletName'
    ]
    
    # Only delete columns that exist in the dataframe
    columns_to_delete = [col for col in columns_to_delete if col in df.columns]
    df = df.drop(columns=columns_to_delete)
    
    # Convert dateTime to mm/dd/yy format
    df['dateTime'] = pd.to_datetime(df['dateTime']).dt.strftime('%m/%d/%y')
    
    # Process feeAmount column - remove quotes and convert to number
    if 'feeAmount' in df.columns:
        df['feeAmount'] = df['feeAmount'].astype(str).str.replace('"', '').replace('', '0')
        df['feeAmount'] = pd.to_numeric(df['feeAmount'], errors='coerce').fillna(0)
    
    # Process FEE operations - move feeAmount to assetAmount and feeAsset to assetTicker
    fee_mask = df['operation'] == 'FEE'
    if fee_mask.any():
        df.loc[fee_mask, 'assetAmount'] = df.loc[fee_mask, 'feeAmount']
        df.loc[fee_mask, 'assetTicker'] = df.loc[fee_mask, 'feeAsset']
    
    # Delete feeAmount and feeAsset columns after processing
    if 'feeAmount' in df.columns:
        df = df.drop(columns=['feeAmount'])
    if 'feeAsset' in df.columns:
        df = df.drop(columns=['feeAsset'])
    
    # Convert WITHDRAW and SELL operations to negative values
    withdraw_sell_mask = df['operation'].isin(['WITHDRAW', 'SELL'])
    if withdraw_sell_mask.any():
        # Only convert positive values to negative (don't reverse already negative values)
        df.loc[withdraw_sell_mask & (df['assetAmount'] > 0), 'assetAmount'] = -df.loc[withdraw_sell_mask & (df['assetAmount'] > 0), 'assetAmount']
        df.loc[withdraw_sell_mask & (df['assetvalueInBaseCurrency'] > 0), 'assetvalueInBaseCurrency'] = -df.loc[withdraw_sell_mask & (df['assetvalueInBaseCurrency'] > 0), 'assetvalueInBaseCurrency']
    
    # Populate Wallet column using walletId lookup
    if 'walletId' in df.columns:
        df['Wallet'] = df['walletId'].map(WALLET_LOOKUP).fillna('')
    else:
        df['Wallet'] = ''
    
    # Rename columns
    df = df.rename(columns={
        'assetvalueInBaseCurrency': 'USD Value',
        'assetAmount': 'Token Amount',
        'parenttransactionId': 'Transaction ID'
    })
    
    # Sort by Transaction ID (oldest first - ascending by dateTime, then by Transaction ID)
    df['dateTime_sort'] = pd.to_datetime(df['dateTime'], format='%m/%d/%y')
    df = df.sort_values(['dateTime_sort', 'Transaction ID'])
    df = df.drop(columns=['dateTime_sort'])
    
    # Insert blank rows between different Transaction IDs
    result_rows = []
    prev_transaction_id = None
    
    for idx, row in df.iterrows():
        current_transaction_id = row['Transaction ID']
        
        # Add blank row if transaction ID changes (except for the first row)
        if prev_transaction_id is not None and current_transaction_id != prev_transaction_id:
            # Create a blank row with same columns
            blank_row = pd.Series(['' for _ in range(len(row))], index=row.index)
            result_rows.append(blank_row)
        
        result_rows.append(row)
        prev_transaction_id = current_transaction_id
    
    # Create new dataframe from rows
    df = pd.DataFrame(result_rows)
    
    # Delete walletId column now that we've populated Wallet
    if 'walletId' in df.columns:
        df = df.drop(columns=['walletId'])
    
    # Reorder columns to specified order
    column_order = [
        'dateTime', 'Wallet', 'Transaction ID', 'operation', 
        'assetTicker', 'Token Amount', 'USD Value', 
        'fromAddress', 'toAddress'
    ]
    
    # Only include columns that exist in the dataframe
    column_order = [col for col in column_order if col in df.columns]
    
    # Add any remaining columns not in the specified order
    remaining_cols = [col for col in df.columns if col not in column_order]
    final_column_order = column_order + remaining_cols
    
    df = df[final_column_order]
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

# Streamlit App
st.set_page_config(page_title="Crypto Transaction Processor", page_icon="💰", layout="wide")

st.title("🔄 Cryptocurrency Transaction Processor")
st.markdown("---")

st.markdown("""
### Instructions:
1. Upload your CSV file containing cryptocurrency transaction data
2. The app will automatically process the data according to predefined rules
3. Review the processed data in the preview below
4. Download the processed CSV file

### Processing Steps:
- Filters for "Uncategorized" transactions only
- Removes unnecessary columns (walletName removed, walletId used for lookup then removed)
- Converts dates to mm/dd/yy format
- Processes FEE operations
- Converts WITHDRAW/SELL amounts to negative values
- Populates "Wallet" column using wallet lookup table
- Groups transactions by Transaction ID with blank row separators
- Sorts with oldest transactions at the top
- Reorders columns for optimal readability
""")

st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        st.success(f"✅ File uploaded successfully! Found {len(df)} total rows.")
        
        # Show original data summary
        with st.expander("📊 Original Data Summary"):
            st.write(f"**Total Rows:** {len(df)}")
            st.write(f"**Columns:** {', '.join(df.columns.tolist())}")
            uncategorized_count = len(df[df['categorizationStatus'] == 'Uncategorized'])
            st.write(f"**Uncategorized Rows:** {uncategorized_count}")
        
        # Process the data
        with st.spinner("Processing transactions..."):
            processed_df = process_crypto_transactions(df)
        
        st.success(f"✅ Processing complete! {len(processed_df)} rows in processed file (including blank separators).")
        
        # Display processed data
        st.markdown("### 📋 Processed Data Preview")
        st.dataframe(processed_df, use_container_width=True, height=400)
        
        # Prepare download
        csv_buffer = io.StringIO()
        processed_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="⬇️ Download Processed CSV",
                data=csv_data,
                file_name=f"processed_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Show statistics
        st.markdown("---")
        st.markdown("### 📈 Transaction Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        # Filter out blank rows for statistics
        stats_df = processed_df[processed_df['Transaction ID'] != ''].copy()
        
        with col1:
            unique_transactions = stats_df['Transaction ID'].nunique()
            st.metric("Unique Transactions", unique_transactions)
        
        with col2:
            operation_counts = stats_df['operation'].value_counts()
            st.metric("Most Common Operation", 
                     f"{operation_counts.index[0]} ({operation_counts.values[0]})" if len(operation_counts) > 0 else "N/A")
        
        with col3:
            total_usd = stats_df['USD Value'].sum()
            st.metric("Total USD Value", f"${total_usd:,.2f}")
        
        with col4:
            unique_assets = stats_df['assetTicker'].nunique()
            st.metric("Unique Assets", unique_assets)
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.exception(e)

else:
    st.info("👆 Please upload a CSV file to begin processing.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Crypto Transaction Processor | Built with Streamlit</small>
</div>
""", unsafe_allow_html=True)
